package dev.practice.assessment01.repository;
import dev.practice.assessment01.model.Ticket;
import org.springframework.data.jpa.repository.JpaRepository;
public interface TicketRepository extends JpaRepository<Ticket,Long>{boolean existsByExternalRef(String externalRef);}
