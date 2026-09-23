package dev.practice.assessment03.repository;
import dev.practice.assessment03.model.Reservation;import org.springframework.data.jpa.repository.JpaRepository;
public interface ReservationRepository extends JpaRepository<Reservation,Long> {java.util.Optional<Reservation> findByRequestKey(String requestKey);}
