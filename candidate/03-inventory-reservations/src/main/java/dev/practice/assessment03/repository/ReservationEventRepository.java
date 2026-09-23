package dev.practice.assessment03.repository;
import dev.practice.assessment03.model.ReservationEvent;import org.springframework.data.jpa.repository.JpaRepository;
public interface ReservationEventRepository extends JpaRepository<ReservationEvent,Long> {}
