package dev.practice.assessment02.support;
import org.springframework.jdbc.core.JdbcTemplate;
public class Fixtures {public static void reset(JdbcTemplate jdbc){jdbc.update("delete from products");jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",106,"NT-02","Plain Notebook","stationery",700,0);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",103,"MS-01","Wireless Mouse","electronics",2500,8);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",110,"CB-01","USB-C Cable","electronics",1000,12);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",101,"KB-01","Compact Keyboard","electronics",5000,5);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",112,"KB-03","Keyboard Cover","accessories",500,10);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",108,"DK-01","Standing Desk","furniture",20000,3);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",104,"MS-02","Travel Mouse","electronics",2500,2);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",111,"ST-01","Monitor Stand","furniture",5000,4);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",102,"KB-02","Mechanical Keyboard","electronics",9000,0);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",109,"CH-01","Office Chair","furniture",15000,0);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",105,"NT-01","Grid Notebook","stationery",700,20);
jdbc.update("insert into products(id,sku,name,category,price_cents,stock) values (?,?,?,?,?,?)",107,"PN-01","Gel Pen","stationery",200,50);}}
