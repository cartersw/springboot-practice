package dev.practice.assessment01.mapper;
import dev.practice.assessment01.model.Ticket;
import dev.practice.assessment01.dto.TicketResponse;
import org.springframework.stereotype.Component;
@Component public class TicketMapper {
 public TicketResponse response(Ticket t){return new TicketResponse(t.getId(),t.getExternalRef(),t.getTitle(),t.getPriority(),t.getStatus().name());}
}
