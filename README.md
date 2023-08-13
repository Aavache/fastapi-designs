<h1 style="text-align: center;">FastAPI Designs</h1>

This repository contains a collection of practical examples demonstrating various concepts and best practices for building powerful APIs using FastAPI. Each example showcases a specific aspect of API development and code samples to help you understand and implement these concepts effectively.

## Installation

Install your dependencies with the following command:

```sh
pip install -r requirements.txt
```

## Available Content

1. [Building blocks](https://github.com/Aavache/fastapi-designs/tree/master/00_building_blocks)
    1. [Pagination](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/00_pagination.py)
    2. [Error handling](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/01_error_handling.py)
    3. [URL Versioning](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/02_url_versioning.py) 
    4. [Header Versioning](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/03_header_versioning.py)
    5. [Caching](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/04_caching.py)
    6. [Deprecation](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/05_deprecation.py)
    7. [Decorator](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/06_decorator.py)
    8. [Decorator for auth](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/06_decorator_auth.py)
    9. [Rate limitter](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/07_rate_limitters.py)
    10. [Filtering and sorting](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/08_filtering_and_sorting.py)
    11. [Bulk operations](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/09_bulk_operations.py)
    12. [Authentification](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/10_authentication.py)
    13. [WebHooks](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/11_webhooks.py)
    14. [Async Polling](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/12_async_polling.py)
    15. [Async Callback](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/13_async_callback.py)
    16. [HATEOAS](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/14_hateoas.py)
    17. [Singleton](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/15_singleton.py)
    18. [Content negotiation](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/16_content_negotiation.py)
    19. [Strategy pattern](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/17_strategy_pattern.py)
    20. [Repository pattern](https://github.com/Aavache/fastapi-designs/blob/master/00_building_blocks/18_repository_pattern.py)
2. [APIs](https://github.com/Aavache/fastapi-designs/tree/master/01_apis)
    1. [RESTful](https://github.com/Aavache/fastapi-designs/blob/master/01_apis/00_restful.py)
    2. [Message Queue](https://github.com/Aavache/fastapi-designs/blob/master/01_apis/01_mesage_queue.py)
    3. [RPC](https://github.com/Aavache/fastapi-designs/blob/master/01_apis/02_rpc.py)
    4. [Event driven](https://github.com/Aavache/fastapi-designs/blob/master/01_apis/03_event_driven.py)
    5. [Hypermedia](https://github.com/Aavache/fastapi-designs/blob/master/01_apis/04_hypermedia.py)
    6. [SOAP](https://github.com/Aavache/fastapi-designs/blob/master/01_apis/05_soap.py)

## Disclaimar

This repository shows some API patterns and building blocks in a simplified manner, therefore it can serve as inspiration for real-case applications however it may require adaption, for instance, for some example we use a in-memory dictionary to similulate a database.

## References

The scripts in this repository are based on the following documentation:
1. [FastAPI](https://fastapi.tiangolo.com/) documentation.
2. [Pika](https://pika.readthedocs.io/en/stable/) documentation.