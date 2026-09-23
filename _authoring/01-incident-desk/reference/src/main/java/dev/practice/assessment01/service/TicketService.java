package dev.practice.assessment01.service;
import java.util.*;
import org.springframework.stereotype.Service;
import dev.practice.assessment01.model.*;
import dev.practice.assessment01.dto.*;
import dev.practice.assessment01.repository.TicketRepository;
import dev.practice.assessment01.mapper.TicketMapper;
import dev.practice.assessment01.validation.TicketRequestValidator;
import dev.practice.assessment01.error.*;
@Service public class TicketService {
 private final TicketRepository repository; private final TicketMapper mapper; private final TicketRequestValidator validator;
 public TicketService(TicketRepository r,TicketMapper m,TicketRequestValidator v){repository=r;mapper=m;validator=v;}
 public TicketResponse create(CreateTicketRequest request){
  String ref=validator.reference(request.externalRef());String title=validator.title(request.title());int priority=validator.priority(request.priority());
  if(repository.existsByExternalRef(ref))throw new DuplicateReferenceException();
  Ticket t=new Ticket();t.setExternalRef(ref);t.setTitle(title);t.setPriority(priority);t.setStatus(TicketStatus.OPEN);
  return mapper.response(repository.saveAndFlush(t));
 }
 private Ticket find(long id){return repository.findById(validator.id(id)).orElseThrow(TicketNotFoundException::new);}
 public TicketResponse get(long id){return mapper.response(find(id));}
 public TicketResponse update(long id,UpdateTicketRequest r){
  validator.id(id);String title=validator.title(r.title());int priority=validator.priority(r.priority());TicketStatus status=validator.status(r.status());
  Ticket t=find(id);t.setTitle(title);t.setPriority(priority);t.setStatus(status);
  return mapper.response(repository.saveAndFlush(t));
 }
 public List<TicketResponse> list(String rawStatus,String rawSort){
  TicketStatus status=rawStatus==null?null:validator.status(rawStatus);TicketSort sort=validator.sort(rawSort);
  Comparator<Ticket> comparator=Comparator.comparing(Ticket::getId);
  if(sort==TicketSort.priorityDesc)comparator=Comparator.comparing(Ticket::getPriority).reversed().thenComparing(Ticket::getId);
  return repository.findAll().stream().filter(t->status==null||t.getStatus()==status).sorted(comparator).map(mapper::response).toList();
 }
 public void delete(long id){Ticket t=find(id);repository.delete(t);}
}
