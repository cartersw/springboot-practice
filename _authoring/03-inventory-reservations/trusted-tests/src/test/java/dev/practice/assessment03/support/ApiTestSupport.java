package dev.practice.assessment03.support;
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
@SpringBootTest @AutoConfigureMockMvc @ActiveProfiles("test") @org.springframework.context.annotation.Import(AuditTestConfig.class)
public abstract class ApiTestSupport {
 @Autowired protected MockMvc mvc;@Autowired protected ObjectMapper mapper;@Autowired protected JdbcTemplate jdbc;
 @Autowired protected ControllableReservationAudit audit;
 @BeforeEach protected void reset(){Fixtures.reset(jdbc);audit.reset();}
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

 protected ObjectNode item(String sku,int quantity){return mapper.createObjectNode().put("sku",sku).put("quantity",quantity);}
 protected ObjectNode request(String key,ObjectNode...items){var b=mapper.createObjectNode().put("requestKey",key).put("customerRef","team-a");var a=b.putArray("items");for(var i:items)a.add(i);return b;}
 protected ObjectNode standard(String key){return request(key,item("BOLT-M8",3),item("NUT-M8",2));}
 protected JsonNode create(Object body,int status)throws Exception{return ok("POST","/api/reservations",body,status);}
 protected JsonNode cancel(long id,int status)throws Exception{return ok("POST","/api/reservations/"+id+"/cancel",null,status);}
 protected List<List<Map<String,Object>>> snapshot(){return List.of(jdbc.queryForList("select * from stock_items order by sku"),jdbc.queryForList("select * from reservations order by id"),jdbc.queryForList("select * from reservation_lines order by id"),jdbc.queryForList("select * from reservation_events order by id"));}
 protected void stock(String sku,int quantity){assertThat(jdbc.queryForObject("select available_quantity from stock_items where sku=?",Integer.class,sku)).isEqualTo(quantity);}
 protected void stocks(int bolt,int nut){stock("BOLT-M8",bolt);stock("NUT-M8",nut);stock("CLIP-S",20);stock("WASHER-M8",0);}
 protected void counts(int headers,int lines,int events){assertThat(jdbc.queryForObject("select count(*) from reservations",Integer.class)).isEqualTo(headers);assertThat(jdbc.queryForObject("select count(*) from reservation_lines",Integer.class)).isEqualTo(lines);assertThat(jdbc.queryForObject("select count(*) from reservation_events",Integer.class)).isEqualTo(events);}
 protected void events(long id,String... values){assertThat(jdbc.queryForList("select event_type from reservation_events where reservation_id=? order by event_type",String.class,id)).containsExactly(values);}
 protected void response(JsonNode n,long id,String key,String customer,String status,String...pairs){shape(n,"id","requestKey","customerRef","status","items","totalQuantity");assertThat(n.path("id").asLong()).isEqualTo(id);assertThat(n.path("requestKey").asText()).isEqualTo(key);assertThat(n.path("customerRef").asText()).isEqualTo(customer);assertThat(n.path("status").asText()).isEqualTo(status);List<String> actual=new ArrayList<>();int total=0;for(var i:n.path("items")){shape(i,"sku","quantity");actual.add(i.path("sku").asText()+"="+i.path("quantity").asInt());total+=i.path("quantity").asInt();}assertThat(actual).containsExactly(pairs);assertThat(n.path("totalQuantity").asInt()).isEqualTo(total);}
 protected void summary(JsonNode n,int[] available,long[] reserved,long[] active){assertThat(n.isArray()).isTrue();String[] skus={"BOLT-M8","CLIP-S","NUT-M8","WASHER-M8"};assertThat(n.size()).isEqualTo(4);for(int i=0;i<4;i++){var r=n.get(i);shape(r,"sku","availableQuantity","reservedQuantity","activeReservations");assertThat(r.path("sku").asText()).isEqualTo(skus[i]);assertThat(r.path("availableQuantity").asInt()).isEqualTo(available[i]);assertThat(r.path("reservedQuantity").isNumber()).isTrue();assertThat(r.path("activeReservations").isNumber()).isTrue();assertThat(r.path("reservedQuantity").asLong()).isEqualTo(reserved[i]);assertThat(r.path("activeReservations").asLong()).isEqualTo(active[i]);}}
 protected void stored(long id,String key,String customer,String status){var r=jdbc.queryForMap("select * from reservations where id=?",id);assertThat(r.get("REQUEST_KEY")).isEqualTo(key);assertThat(r.get("CUSTOMER_REF")).isEqualTo(customer);assertThat(r.get("STATUS")).isEqualTo(status);}
 protected void persistedLines(long id,String... expected){assertThat(jdbc.query("select sku,quantity from reservation_lines where reservation_id=? order by sku",(rs,i)->rs.getString(1)+"="+rs.getInt(2),id)).containsExactly(expected);}
}
