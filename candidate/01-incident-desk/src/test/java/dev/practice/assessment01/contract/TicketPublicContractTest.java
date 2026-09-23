package dev.practice.assessment01.contract;
import dev.practice.assessment01.support.ApiTestSupport;
import java.util.*;
import org.junit.jupiter.api.*;
import static org.assertj.core.api.Assertions.assertThat;
public class TicketPublicContractTest extends ApiTestSupport {
 @Test @DisplayName("Existing ticket representation") void a1_01() throws Exception { var before=snapshot();ticket(ok("GET","/api/tickets/101",null,200),101,"INC-101","Printer offline",3,"OPEN");assertThat(snapshot()).isEqualTo(before); }
 @Test @DisplayName("Default ordered collection") void a1_02() throws Exception { var n=ok("GET","/api/tickets",null,200);assertThat(ids(n)).containsExactly(101L,102L,103L,104L);n.forEach(x->shape(x,"id","externalRef","title","priority","status")); }
 @Test @DisplayName("Create and persist") void a1_03() throws Exception { var r=req("POST","/api/tickets",create("INC-200"));assertThat(r.getResponse().getStatus()).isEqualTo(201);var n=json(r);long id=n.path("id").asLong();assertThat(id).isPositive().isNotIn(101L,102L,103L,104L);assertThat(r.getResponse().getHeader("Location")).isEqualTo("/api/tickets/"+id);ticket(n,id,"INC-200","New incident",2,"OPEN");stored(id,"INC-200","New incident",2,"OPEN");count(5); }
 @Test @DisplayName("Normalize create and ignore read only input") void a1_04() throws Exception { var b=create(" inc-201 ").put("title","  Scanner disconnected  ").put("priority",4).put("id",999999).put("status","RESOLVED");var n=ok("POST","/api/tickets",b,201);long id=n.path("id").asLong();assertThat(id).isPositive().isNotEqualTo(999999);ticket(n,id,"INC-201","Scanner disconnected",4,"OPEN");stored(id,"INC-201","Scanner disconnected",4,"OPEN");count(5); }
 @Test @DisplayName("Missing ticket") void a1_05() throws Exception { error("GET","/api/tickets/9999",null,404,"NOT_FOUND");count(4); }
 @Test @DisplayName("Duplicate reference") void a1_06() throws Exception { var before=snapshot();error("POST","/api/tickets",create("INC-101"),409,"DUPLICATE_REFERENCE");assertThat(snapshot()).isEqualTo(before); }
 @Test @DisplayName("Replace mutable fields") void a1_07() throws Exception { var n=ok("PUT","/api/tickets/101",update().put("title","  Connection repaired ").put("priority",2).put("status"," resolved "),200);ticket(n,101,"INC-101","Connection repaired",2,"RESOLVED");stored(101,"INC-101","Connection repaired",2,"RESOLVED"); }
 @Test @DisplayName("Missing update") void a1_08() throws Exception { var before=snapshot();error("PUT","/api/tickets/9999",update(),404,"NOT_FOUND");assertThat(snapshot()).isEqualTo(before); }
 @Test @DisplayName("Delete existing") void a1_09() throws Exception { var r=req("DELETE","/api/tickets/102",null);assertThat(r.getResponse().getStatus()).isEqualTo(204);assertThat(r.getResponse().getContentAsByteArray()).isEmpty();assertThat(jdbc.queryForList("select id from tickets order by id",Long.class)).containsExactly(101L,103L,104L); }
 @Test @DisplayName("Missing delete") void a1_10() throws Exception { var before=snapshot();error("DELETE","/api/tickets/9999",null,404,"NOT_FOUND");assertThat(snapshot()).isEqualTo(before); }
 @Test @DisplayName("Status filtering") void a1_11() throws Exception { assertThat(ids(ok("GET","/api/tickets?status=OPEN",null,200))).containsExactly(101L,103L); }
 @Test @DisplayName("Priority ordering") void a1_12() throws Exception { assertThat(ids(ok("GET","/api/tickets?sort=priorityDesc",null,200))).containsExactly(103L,101L,104L,102L); }
 @Test @DisplayName("Filter and ordering") void a1_13() throws Exception { assertThat(ids(ok("GET","/api/tickets?status=OPEN&sort=priorityDesc",null,200))).containsExactly(103L,101L); }
 @Test @DisplayName("Invalid create boundaries") void a1_14() throws Exception { var before=snapshot();for(var b:List.of(create("INC-200").put("title","   "),create("  "),create("INC-200").put("priority",0),create("INC-200").put("priority",6))) {error("POST","/api/tickets",b,400,"INVALID_REQUEST");assertThat(snapshot()).isEqualTo(before);} }
 @Test @DisplayName("Invalid JSON and integer input") void a1_15() throws Exception { var before=snapshot();for(Object b:List.of("{\"title\":\"a\"",create("INC-200").put("priority","abc"),create("INC-200").put("priority",2.5))) {error("POST","/api/tickets",b,400,"INVALID_REQUEST");assertThat(snapshot()).isEqualTo(before);} }
}
