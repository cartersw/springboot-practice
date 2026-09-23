package dev.practice.assessment03.audit;
import org.springframework.stereotype.Component;import dev.practice.assessment03.repository.*;import dev.practice.assessment03.model.ReservationEvent;
@Component("databaseReservationAudit") public class DatabaseReservationAudit implements ReservationAudit {
 private final ReservationEventRepository events;private final ReservationRepository reservations;
 public DatabaseReservationAudit(ReservationEventRepository e,ReservationRepository r){events=e;reservations=r;}
 private void record(long id,String type){var event=new ReservationEvent();event.setReservation(reservations.findById(id).orElseThrow());event.setEventType(type);events.saveAndFlush(event);}
 public void recordCreated(long id){record(id,"CREATED");}public void recordCancelled(long id){record(id,"CANCELLED");}
}
