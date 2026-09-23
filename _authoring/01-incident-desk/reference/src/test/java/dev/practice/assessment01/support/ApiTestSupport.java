package dev.practice.assessment01.support;
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
@SpringBootTest @AutoConfigureMockMvc @ActiveProfiles("test")
public abstract class ApiTestSupport {
 @Autowired protected MockMvc mvc;@Autowired protected ObjectMapper mapper;@Autowired protected JdbcTemplate jdbc;
 @BeforeEach protected void reset(){Fixtures.reset(jdbc);}
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
 protected ObjectNode create(String ref){return mapper.createObjectNode().put("externalRef",ref).put("title","New incident").put("priority",2);}
 protected ObjectNode update(){return mapper.createObjectNode().put("title","Edited title").put("priority",4).put("status","OPEN");}
 protected List<Map<String,Object>> snapshot(){return jdbc.queryForList("select * from tickets order by id");}
 protected void count(int n){assertThat(jdbc.queryForObject("select count(*) from tickets",Integer.class)).isEqualTo(n);}
 protected JsonNode row(long id){return mapper.valueToTree(jdbc.queryForMap("select id,external_ref,title,priority,status from tickets where id=?",id));}
 protected void ticket(JsonNode n,long id,String ref,String title,int priority,String status){shape(n,"id","externalRef","title","priority","status");assertThat(n.path("id").asLong()).isEqualTo(id);assertThat(n.path("externalRef").asText()).isEqualTo(ref);assertThat(n.path("title").asText()).isEqualTo(title);assertThat(n.path("priority").asInt()).isEqualTo(priority);assertThat(n.path("status").asText()).isEqualTo(status);}
 protected void stored(long id,String ref,String title,int priority,String status){var r=jdbc.queryForMap("select * from tickets where id=?",id);assertThat(r.get("EXTERNAL_REF")).isEqualTo(ref);assertThat(r.get("TITLE")).isEqualTo(title);assertThat(((Number)r.get("PRIORITY")).intValue()).isEqualTo(priority);assertThat(r.get("STATUS")).isEqualTo(status);}
}
