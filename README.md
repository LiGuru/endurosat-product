## EnduroSat

- [Task#1](documentation/endurosat-protocol-description.md)
    - [Diagram](documentation/endurosat.puml)
    - [Protocols](documentation/endurosat-protocol-description.md)

- Releases
  - [UHF_TASK](documentation/UHF_TASK.md)
  - [Antenna_TASK](documentation/Antenna_TASK.md)

### Approach

```
.
├── application
│   ├── services
│   └── use_cases
├── documentation
├── domain
│   ├── interfaces
│   └── model
│       ├── decoders
│       ├── encoders
│       └── hardware
├── external_services
│   └── uart
├── infrastructure
│   ├── commons
│   ├── config
│   ├── helpers
│   ├── logging
│   └── wrappers
├── logs
└── tests
```

The project structure is organized as follows:

    application: Contains the main logic of the application, divided into two subdirectories - services and use_cases.
        services: Includes modules responsible for various services and integrations.
        use_cases: Contains modules that implement the business logic of the application.

    documentation: Contains project documentation.

    domain: Includes models and interfaces defining the data structure and interactions in the application.
        interfaces: Contains interfaces that describe contracts for interaction between different components.
        model: Contains models of the application representing the data structure.
            decoders: Modules for decoding data.
            encoders: Modules for encoding data.
            hardware: Modules related to hardware components.

    external_services: Includes external services or integrations, such as a service for managing UART.

    infrastructure: Contains code related to infrastructure, such as logs, configurations, and helper functions.
        commons: Contains common modules and tools used in various parts of the project.
        config: Includes modules for configuring the application.
        helpers: Contains helper functions and modules.
        logging: Includes modules for logs.
        wrappers: Wrappers and helper modules.

    logs: Contains log files from the execution of the application.

    tests: Includes tests for different components of the application.

Architecture:

The project follows a modular and clean architecture, separating concerns into distinct layers. This approach enhances readability, maintainability, and testability. Key architectural principles include:

    Separation of Concerns: Each layer has a specific responsibility, and components within a layer are focused on a single concern.

    Dependency Inversion: Higher-level layers (e.g., application, external_services) depend on abstractions defined in lower-level layers (domain, infrastructure).

    Testability: The modular structure facilitates unit testing, with each module representing a testable component.

    Flexibility and Extensibility: The architecture allows for easy extension or modification of components without affecting other parts of the system.

This architecture provides a foundation for building a scalable and maintainable application, with clear boundaries between different parts of the system.

