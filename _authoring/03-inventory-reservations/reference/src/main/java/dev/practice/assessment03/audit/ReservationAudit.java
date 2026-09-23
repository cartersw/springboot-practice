package dev.practice.assessment03.audit;
public interface ReservationAudit {void recordCreated(long reservationId);void recordCancelled(long reservationId);}
