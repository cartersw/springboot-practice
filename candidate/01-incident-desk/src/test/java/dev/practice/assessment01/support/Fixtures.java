package dev.practice.assessment01.support;
import org.springframework.jdbc.core.JdbcTemplate;
public class Fixtures {public static void reset(JdbcTemplate jdbc){jdbc.update("delete from tickets");jdbc.update("insert into tickets(id,external_ref,title,priority,status) values (104,'INC-104','Dashboard delay',3,'RESOLVED'),(102,'INC-102','Scanner timeout',1,'IN_PROGRESS'),(103,'INC-103','Label mismatch',5,'OPEN'),(101,'INC-101','Printer offline',3,'OPEN')");}}
