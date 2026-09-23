package dev.practice.assessment02.controller;
import org.springframework.web.bind.annotation.*;
import dev.practice.assessment02.service.ProductWriteService;import dev.practice.assessment02.dto.*;
@RestController public class ProductWriteController {
 private final ProductWriteService service;public ProductWriteController(ProductWriteService s){service=s;}
 @PutMapping("/api/products/{id}") public ProductResponse update(@PathVariable long id,@RequestBody UpdateProductRequest r){return service.update(id,r);}
}
