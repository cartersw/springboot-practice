package dev.practice.assessment03.support;
import org.springframework.jdbc.core.JdbcTemplate;
public class Fixtures {
 public static void reset(JdbcTemplate jdbc){jdbc.update("delete from reservation_events");jdbc.update("delete from reservation_lines");jdbc.update("delete from reservations");jdbc.update("delete from stock_items");jdbc.update("insert into stock_items(sku,display_name,available_quantity) values ('WASHER-M8','M8 Washer',0),('NUT-M8','M8 Nut',8),('CLIP-S','Small Clip',20),('BOLT-M8','M8 Bolt',10)");}
 public static void reservation(JdbcTemplate jdbc,long id,String key,String customer,String status,String canonical){jdbc.update("insert into reservations(id,request_key,customer_ref,status,canonical_payload) values (?,?,?,?,?)",id,key,customer,status,canonical);}
 public static void line(JdbcTemplate jdbc,long id,long reservation,String sku,int quantity){jdbc.update("insert into reservation_lines(id,reservation_id,sku,quantity) values (?,?,?,?)",id,reservation,sku,quantity);}
 public static void event(JdbcTemplate jdbc,long id,long reservation,String type){jdbc.update("insert into reservation_events(id,reservation_id,event_type) values (?,?,?)",id,reservation,type);}
 public static void active701(JdbcTemplate jdbc){reservation(jdbc,701,"fixture-701","team-a","ACTIVE","[\"team-a\",[[\"BOLT-M8\",3],[\"NUT-M8\",2]]]");line(jdbc,711,701,"BOLT-M8",3);line(jdbc,712,701,"NUT-M8",2);event(jdbc,721,701,"CREATED");jdbc.update("update stock_items set available_quantity=7 where sku='BOLT-M8'");jdbc.update("update stock_items set available_quantity=6 where sku='NUT-M8'");}
 public static void cancelled701(JdbcTemplate jdbc){active701(jdbc);jdbc.update("update reservations set status='CANCELLED' where id=701");jdbc.update("update stock_items set available_quantity=10 where sku='BOLT-M8'");jdbc.update("update stock_items set available_quantity=8 where sku='NUT-M8'");event(jdbc,722,701,"CANCELLED");}
}
