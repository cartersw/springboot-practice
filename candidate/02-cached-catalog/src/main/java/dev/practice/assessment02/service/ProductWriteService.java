package dev.practice.assessment02.service;
import java.util.Locale;import org.springframework.stereotype.Service;
import dev.practice.assessment02.dto.*;import dev.practice.assessment02.error.*;import dev.practice.assessment02.repository.ProductRepository;import dev.practice.assessment02.cache.SearchCacheInvalidator;
@Service public class ProductWriteService {
 private final ProductRepository repository;private final SearchCacheInvalidator invalidator;
 public ProductWriteService(ProductRepository r,SearchCacheInvalidator i){repository=r;invalidator=i;}
 public ProductResponse update(long id,UpdateProductRequest r){
  if(id<=0)throw new InvalidRequestException("ID must be positive");
  if(r.name()==null||r.name().strip().isEmpty()||r.name().strip().length()>100)throw new InvalidRequestException("Invalid name");
  if(r.category()==null)throw new InvalidRequestException("Category required");String category=r.category().strip().toLowerCase(Locale.ROOT);
  if(category.length()>40||!category.matches("[a-z][a-z0-9-]*"))throw new InvalidRequestException("Invalid category");
  if(r.priceCents()==null||r.priceCents()<0||r.priceCents()>1000000000||r.stock()==null||r.stock()<0||r.stock()>1000000)throw new InvalidRequestException("Invalid price or stock");
  var p=repository.findById(id).orElseThrow(ProductNotFoundException::new);p.setName(r.name().strip());p.setCategory(category);p.setPriceCents(r.priceCents());p.setStock(r.stock());
  var saved=repository.saveAndFlush(p);invalidator.invalidate();return ProductResponse.from(saved);
 }
}
