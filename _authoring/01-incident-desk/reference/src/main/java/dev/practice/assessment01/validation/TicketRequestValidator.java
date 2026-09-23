package dev.practice.assessment01.validation;
import java.util.Locale;
import dev.practice.assessment01.error.InvalidRequestException;
import dev.practice.assessment01.model.*;
import org.springframework.stereotype.Component;
@Component public class TicketRequestValidator {
 public long id(long id){if(id<=0)throw new InvalidRequestException("ID must be positive");return id;}
 public String title(String s){if(s==null||s.strip().isEmpty()||s.strip().length()>120)throw new InvalidRequestException("Invalid title");return s.strip();}
 public String reference(String s){if(s==null)throw new InvalidRequestException("Reference required");String v=s.strip().toUpperCase(Locale.ROOT);if(!v.matches("[A-Z0-9-]{3,32}"))throw new InvalidRequestException("Invalid reference");return v;}
 public int priority(Integer p){if(p==null||p<1||p>5)throw new InvalidRequestException("Invalid priority");return p;}
 public TicketStatus status(String s){try{return TicketStatus.valueOf(s.strip().toUpperCase(Locale.ROOT));}catch(Exception e){throw new InvalidRequestException("Invalid status");}}
 public TicketSort sort(String s){try{return s==null?TicketSort.idAsc:TicketSort.valueOf(s.strip());}catch(Exception e){throw new InvalidRequestException("Invalid sort");}}
}
