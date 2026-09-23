package dev.practice.assessment02.controller;
import java.util.Map;import org.springframework.web.bind.annotation.*;
import dev.practice.assessment02.service.ProductSearchService;import dev.practice.assessment02.search.SearchRequestParser;import dev.practice.assessment02.dto.CatalogPageResponse;
@RestController public class ProductSearchController {
 private final ProductSearchService service;private final SearchRequestParser parser;
 public ProductSearchController(ProductSearchService s,SearchRequestParser p){service=s;parser=p;}
 @GetMapping("/api/products") public CatalogPageResponse search(@RequestParam Map<String,String> params){return service.search(parser.parse(params));}
}
