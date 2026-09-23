package dev.practice.assessment01.model;
import jakarta.persistence.*;
@Entity @Table(name="tickets")
public class Ticket {
 @Id @GeneratedValue(strategy=GenerationType.SEQUENCE,generator="ticket_seq")
 @SequenceGenerator(name="ticket_seq",sequenceName="ticket_seq",allocationSize=1,initialValue=1000)
 private Long id;
 @Column(name="external_ref",nullable=false,unique=true,length=32) private String externalRef;
 @Column(nullable=false,length=120) private String title;
 @Column(nullable=false) private Integer priority;
 @Enumerated(EnumType.STRING) @Column(nullable=false) private TicketStatus status;
 public Ticket() {}
 public Long getId(){return id;} public void setId(Long v){id=v;}
 public String getExternalRef(){return externalRef;} public void setExternalRef(String v){externalRef=v;}
 public String getTitle(){return title;} public void setTitle(String v){title=v;}
 public Integer getPriority(){return priority;} public void setPriority(Integer v){priority=v;}
 public TicketStatus getStatus(){return status;} public void setStatus(TicketStatus v){status=v;}
}
