package dev.practice.assessment02.repository;
import dev.practice.assessment02.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
public interface ProductRepository extends JpaRepository<Product,Long> {}
