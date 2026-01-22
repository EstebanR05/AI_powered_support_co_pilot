# 🏗️ Architectural Decision Records (ADR)

## ADR-001: Hexagonal Architecture

**Status**: Accepted  
**Date**: 2024-01-21

### Context
We need to build a scalable microservice that can easily adapt to different external services (databases, AI providers, notification systems) while maintaining clean business logic.

### Decision
Implement Hexagonal Architecture (Ports and Adapters pattern) with the following structure:

- **Domain**: Core business logic and entities
- **Ports**: Interfaces defining contracts
- **Adapters**: Concrete implementations of external services
- **Application**: Use cases orchestrating business operations
- **Infrastructure**: Web controllers, configuration, dependency injection

### Consequences
**Pros**:
- Testability: Easy to mock dependencies
- Flexibility: Can swap implementations without changing core logic
- Maintainability: Clear separation of concerns
- Scalability: Each layer can evolve independently

**Cons**:
- Initial complexity higher than simple layered architecture
- More files and abstractions to manage

---

## ADR-002: Dependency Injection Container

**Status**: Accepted  
**Date**: 2024-01-21

### Context
Need to manage dependencies between layers without tight coupling.

### Decision
Implement manual dependency injection using a Container class with lazy loading.

### Consequences
- Clean dependency management
- Easy to configure different implementations for different environments
- No external DI framework dependency

---

## ADR-003: Domain-Driven Design Entities

**Status**: Accepted  
**Date**: 2024-01-21

### Context
Need to model business concepts clearly and enforce business rules.

### Decision
Use DDD approach with:
- Entities with business logic methods
- Value Objects for immutable data
- Factory methods for object creation
- Enums for constrained values

### Consequences
- Self-documenting code
- Business rules centralized in domain
- Type safety with enums

---

## ADR-004: Async/Await Pattern

**Status**: Accepted  
**Date**: 2024-01-21

### Context
Need to handle I/O operations efficiently (database, AI API calls, webhooks).

### Decision
Use async/await throughout the application stack.

### Consequences
- Better performance for I/O bound operations
- Consistent async interface
- Compatible with FastAPI async features

---

## ADR-005: Repository Pattern

**Status**: Accepted  
**Date**: 2024-01-21

### Context
Need to abstract data persistence and allow easy switching between in-memory and Supabase storage.

### Decision
Implement Repository pattern with port interface and multiple adapters.

### Consequences
- Easy testing with in-memory implementation
- Production ready with Supabase
- Database agnostic business logic