package dev.practice.assessment01.controller;
import java.net.URI;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import dev.practice.assessment01.service.TicketService;
import dev.practice.assessment01.dto.*;
@RestController @RequestMapping("/api/tickets") public class TicketController {
 private final TicketService service;
 public TicketController(TicketService s){service=s;}
 @PostMapping public ResponseEntity<TicketResponse> create(@RequestBody CreateTicketRequest r){TicketResponse t=service.create(r);return ResponseEntity.status(201).location(URI.create("/api/tickets/"+t.id())).body(t);}
 @GetMapping("/{id}") public ResponseEntity<TicketResponse> get(@PathVariable long id){return ResponseEntity.ok(service.get(id));}
 @GetMapping public List<TicketResponse> list(@RequestParam(required=false) String status,@RequestParam(required=false) String sort){return service.list(status,sort);}
 @PutMapping("/{id}") public TicketResponse update(@PathVariable long id,@RequestBody UpdateTicketRequest r){return service.update(id,r);}
 @DeleteMapping("/{id}") public ResponseEntity<Void> delete(@PathVariable long id){service.delete(id);return ResponseEntity.noContent().build();}
}
