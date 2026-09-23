package dev.practice.assessment02.contract;
import dev.practice.assessment02.support.ApiTestSupport;
import org.junit.jupiter.api.Test;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.assertj.core.api.Assertions.assertThat;
public class SmokeTest extends ApiTestSupport {
 @Test void contextStarts(){assertThat(mvc).isNotNull();}
 @Test void healthResponds() throws Exception {mvc.perform(get("/health")).andExpect(status().isOk()).andExpect(org.springframework.test.web.servlet.result.MockMvcResultMatchers.content().json("{\"status\":\"UP\"}"));}
}
