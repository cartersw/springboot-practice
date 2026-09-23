package dev.practice.assessment02.support;
import java.util.*;
import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.*;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import static org.assertj.core.api.Assertions.assertThat;
@SpringBootTest @AutoConfigureMockMvc @ActiveProfiles("test") @org.springframework.context.annotation.Import(ClockTestConfig.class)
public abstract class ApiTestSupport {
 @Autowired protected MockMvc mvc;@Autowired protected ObjectMapper mapper;@Autowired protected JdbcTemplate jdbc;
 @Autowired protected dev.practice.assessment02.cache.KeyValueStore cache;@Autowired protected dev.practice.assessment02.observation.QueryProbe probe;@Autowired protected MutableClock clock;
 @BeforeEach protected void reset(){Fixtures.reset(jdbc);clock.reset();cacheReset();}
 protected MvcResult req(String method,String path,Object body) throws Exception {
  var b=MockMvcRequestBuilders.request(org.springframework.http.HttpMethod.valueOf(method),path);
  if(body!=null)b.contentType(MediaType.APPLICATION_JSON).content(body instanceof String?(String)body:mapper.writeValueAsString(body));
  return mvc.perform(b).andReturn();
 }
 protected JsonNode json(MvcResult r)throws Exception{return mapper.readTree(r.getResponse().getContentAsString());}
 protected JsonNode ok(String method,String path,Object body,int status)throws Exception{var r=req(method,path,body);assertThat(r.getResponse().getStatus()).isEqualTo(status);return json(r);}
 protected void error(String method,String path,Object body,int status,String code)throws Exception{
  var r=req(method,path,body);assertThat(r.getResponse().getStatus()).isEqualTo(status);JsonNode n=json(r);
  shape(n,"status","code","message","path");assertThat(n.get("status").asInt()).isEqualTo(status);assertThat(n.get("code").asText()).isEqualTo(code);assertThat(n.get("message").asText()).isNotBlank();assertThat(n.get("path").asText()).isEqualTo(path.split("\\?",2)[0]);
 }
 protected void shape(JsonNode n,String... names){
  assertThat(n.isObject()).isTrue();Set<String>s=new HashSet<>();n.fieldNames().forEachRemaining(s::add);assertThat(s).containsExactlyInAnyOrder(names);
  for(String name:names){var value=n.get(name);
   if(Set.of("id","priority","priceCents","stock","page","size","totalElements","totalPages","quantity","totalQuantity","availableQuantity","reservedQuantity","activeReservations").contains(name)||(name.equals("status")&&n.has("code")))assertThat(value.isIntegralNumber()).as(name+" is a JSON integer").isTrue();
   else if(Set.of("first","last").contains(name))assertThat(value.isBoolean()).as(name+" is a JSON boolean").isTrue();
   else if(Set.of("items","content").contains(name))assertThat(value.isArray()).as(name+" is a JSON array").isTrue();
   else assertThat(value.isTextual()).as(name+" is a JSON string").isTrue();
  }
 }
 protected List<Long> ids(JsonNode n){assertThat(n.isArray()).isTrue();List<Long>r=new ArrayList<>();n.forEach(x->{assertThat(x.path("id").isIntegralNumber()).isTrue();r.add(x.get("id").asLong());});return r;}
 protected ObjectNode update(){return mapper.createObjectNode().put("name","Wireless Mouse").put("category","electronics").put("priceCents",2500).put("stock",8);}
 protected List<Map<String,Object>> snapshot(){return jdbc.queryForList("select * from products order by id");}
 protected JsonNode search(String query)throws Exception{return ok("GET","/api/products"+(query.isEmpty()?"":"?"+query),null,200);}
 protected void content(JsonNode n,Long... values){assertThat(ids(n.path("content"))).containsExactly(values);}
 protected void calls(long n){assertThat(probe.calls()).isEqualTo(n);}
 protected void cacheReset(){for(String k:cache.keys())cache.delete(k);probe.reset();}
 protected void metadata(JsonNode n,int page,int size,long total,int pages,boolean first,boolean last){shape(n,"content","page","size","totalElements","totalPages","first","last");assertThat(n.path("page").asInt()).isEqualTo(page);assertThat(n.path("size").asInt()).isEqualTo(size);assertThat(n.path("totalElements").asLong()).isEqualTo(total);assertThat(n.path("totalPages").asInt()).isEqualTo(pages);assertThat(n.path("first").asBoolean()).isEqualTo(first);assertThat(n.path("last").asBoolean()).isEqualTo(last);}
}
