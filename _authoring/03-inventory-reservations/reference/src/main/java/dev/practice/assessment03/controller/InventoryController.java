package dev.practice.assessment03.controller;
import java.util.List;import org.springframework.web.bind.annotation.*;import dev.practice.assessment03.dto.InventorySummaryResponse;import dev.practice.assessment03.repository.InventorySummaryRepository;
@RestController public class InventoryController {private final InventorySummaryRepository repository;public InventoryController(InventorySummaryRepository r){repository=r;}@GetMapping("/api/inventory/summary") public List<InventorySummaryResponse> summary(){return repository.summary();}}
