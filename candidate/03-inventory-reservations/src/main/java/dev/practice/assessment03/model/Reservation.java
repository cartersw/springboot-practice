package dev.practice.assessment03.model;
import jakarta.persistence.*;
@Entity @Table(name="reservations") public class Reservation {
 @Id @GeneratedValue(strategy=GenerationType.SEQUENCE,generator="reservation_seq")
 @SequenceGenerator(name="reservation_seq",sequenceName="reservation_seq",allocationSize=1,initialValue=1000) private Long id;
 @Column(name="request_key",nullable=false,unique=true,length=64) private String requestKey;
 @Column(name="customer_ref",nullable=false,length=64) private String customerRef;
 @Enumerated(EnumType.STRING) @Column(nullable=false) private ReservationStatus status;
 @Column(name="canonical_payload",nullable=false,length=4096) private String canonicalPayload;
 public Reservation(){}
 public Long getId(){return id;}public void setId(Long v){id=v;}
 public String getRequestKey(){return requestKey;}public void setRequestKey(String v){requestKey=v;}
 public String getCustomerRef(){return customerRef;}public void setCustomerRef(String v){customerRef=v;}
 public ReservationStatus getStatus(){return status;}public void setStatus(ReservationStatus v){status=v;}
 public String getCanonicalPayload(){return canonicalPayload;}public void setCanonicalPayload(String v){canonicalPayload=v;}
}
