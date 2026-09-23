package dev.practice.assessment03.support;
import org.springframework.boot.test.context.TestConfiguration;import org.springframework.context.annotation.*;import org.springframework.beans.factory.annotation.Qualifier;import dev.practice.assessment03.audit.ReservationAudit;
@TestConfiguration public class AuditTestConfig {@Bean @Primary public ControllableReservationAudit controlledAudit(@Qualifier("databaseReservationAudit") ReservationAudit real){return new ControllableReservationAudit(real);}}
