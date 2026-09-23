package dev.practice.assessment01.config;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import org.springframework.boot.CommandLineRunner;
import org.springframework.jdbc.core.JdbcTemplate;
@Component @Profile("demo") public class DemoDataInitializer implements CommandLineRunner {
 private final JdbcTemplate jdbc;public DemoDataInitializer(JdbcTemplate j){jdbc=j;}
 public void run(String... args){jdbc.update("insert into tickets(id,external_ref,title,priority,status) values (104,'INC-104','Dashboard delay',3,'RESOLVED'),(102,'INC-102','Scanner timeout',1,'IN_PROGRESS'),(103,'INC-103','Label mismatch',5,'OPEN'),(101,'INC-101','Printer offline',3,'OPEN')");}
}
