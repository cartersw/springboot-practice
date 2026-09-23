package dev.practice.assessment03.controller;
import java.net.URI;import org.springframework.web.bind.annotation.*;import org.springframework.http.ResponseEntity;import dev.practice.assessment03.dto.*;import dev.practice.assessment03.service.ReservationService;
@RestController @RequestMapping("/api/reservations") public class ReservationController {
 private final ReservationService service;public ReservationController(ReservationService s){service=s;}
 @PostMapping public ResponseEntity<ReservationResponse> create(@RequestBody CreateReservationRequest r){var outcome=service.create(r);var body=outcome.reservation();return ResponseEntity.status(201).location(URI.create("/api/reservations/"+body.id())).body(body);}
 @GetMapping("/{id}") public ReservationResponse get(@PathVariable long id){return service.get(id);}
 @PostMapping("/{id}/cancel") public ReservationResponse cancel(@PathVariable long id){return service.cancel(id);}
}
