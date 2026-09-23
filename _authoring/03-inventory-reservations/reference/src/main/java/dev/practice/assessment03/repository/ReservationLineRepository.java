package dev.practice.assessment03.repository;
import dev.practice.assessment03.model.ReservationLine;import org.springframework.data.jpa.repository.JpaRepository;
public interface ReservationLineRepository extends JpaRepository<ReservationLine,Long> {java.util.List<ReservationLine> findByReservationIdOrderByStockItemSkuAsc(long reservationId);}
