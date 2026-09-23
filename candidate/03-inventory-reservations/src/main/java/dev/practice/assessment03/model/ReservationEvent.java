package dev.practice.assessment03.model;
import jakarta.persistence.*;import org.hibernate.annotations.Check;
@Entity @Table(name="reservation_events") @Check(constraints="event_type in ('CREATED','CANCELLED')") public class ReservationEvent {
 @Id @GeneratedValue(strategy=GenerationType.SEQUENCE,generator="reservation_event_seq")
 @SequenceGenerator(name="reservation_event_seq",sequenceName="reservation_event_seq",allocationSize=1,initialValue=1000) private Long id;
 @ManyToOne(optional=false) @JoinColumn(name="reservation_id",nullable=false) private Reservation reservation;
 @Column(name="event_type",nullable=false) private String eventType;
 public ReservationEvent(){}
 public Long getId(){return id;}public void setId(Long v){id=v;}
 public Reservation getReservation(){return reservation;}public void setReservation(Reservation v){reservation=v;}
 public String getEventType(){return eventType;}public void setEventType(String v){eventType=v;}
}
