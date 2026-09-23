package dev.practice.assessment03.support;
import dev.practice.assessment03.audit.ReservationAudit;import dev.practice.assessment03.error.AuditUnavailableException;
public class ControllableReservationAudit implements ReservationAudit {
 private final ReservationAudit delegate;private boolean created,cancelled;public ControllableReservationAudit(ReservationAudit d){delegate=d;}
 public void reset(){created=false;cancelled=false;}public void failNextCreated(){created=true;}public void failNextCancelled(){cancelled=true;}
 public void recordCreated(long id){if(created){created=false;throw new AuditUnavailableException();}delegate.recordCreated(id);}
 public void recordCancelled(long id){if(cancelled){cancelled=false;throw new AuditUnavailableException();}delegate.recordCancelled(id);}
}
