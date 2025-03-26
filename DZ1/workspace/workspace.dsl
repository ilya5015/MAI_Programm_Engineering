workspace "Система заказа услуг" {

    name "Система заказа услуг"
    !docs documentation
    !adrs decisions

    model {
        # person
        customer = person "Customer"
        contractor = person "Contractor"

        # software system
        order_system = softwareSystem "Order_system" {
            # Контейнеры (C2)
            webApp = container "Web_Application" {
                description "Provides functionality for customers and contractors via web browser."
                technology "React"
            }

            apiApplication = container "API_application" {
                description "Provides functionality for customers and contractors via a JSON/HTTPS API."
                technology "Python, FastAPI"

                apiGateway = component "API_Gateway" {
                    description "Объединяет и маршрутизирует запросы к различным сервисам, обеспечивая единую точку входа для клиентов и защищая внутреннюю инфраструктуру"
                }

                userService = component "User_service" {
                    description "Регистрация и авторизация пользователей, проверка jwt, получение информации о пользователях"
                }

                serviceComponent = component "Service_component" {
                    description "Предоставляет функционал для работы с услугами: получение списка услуг, создание новой услуги"
                } 
                
                orderingService = component "Ordering_service" {
                    description "Предоставляет функционал для работы с заказами покупателей: добавление услуг в заказ, получение заказа пользователя"
                }                 
            }

            database = container "Database" {
                description "Stores customers and contractors information, authentification credentials, services data, etc."
                technology "PostgreSQL"
            }
        }

        # С1 conns
        customer -> order_system "Регистрация, авторизация, получение списка услуг, создание заказа с услугами"
        contractor -> order_system "Регистрация, авторизация, размещение услуги"

        # C2 conns
        customer -> webApp "Взаимодействует с функционалом сервиса для покупателей: регистрируется, авторизируется, получает список услуг, заказывает услуги"
        contractor -> webApp "Взаимодействует с функционалом сервиса для подрядчиков: регистрируется, авторизируется, размещает услуги"
        webApp -> apiApplication "Делает api запросы" "JSON/HTTPS"
        apiApplication -> Database "Читает и сохраняет данные"

        # C3 conns
        orderingService -> Database "CRUD"
        serviceComponent -> Database "CRUD"
        userService -> Database "CRUD"
        apiGateway -> userService
        apiGateway -> serviceComponent
        apiGateway -> orderingService
        }

    views {
    themes default

    dynamic order_system "uc1" "Создать заказ с услугой" {
            autoLayout lr

            customer -> webApp "Создает заказ с услугой"
            webApp -> apiApplication "Создает запрос на создание нового заказа для пользователя"
            apiApplication -> database "Сохраняет данные о новом заказе"
            apiApplication -> webApp "Создает ответ на запрос о создании заказа"
            webApp -> customer "Оповещает об удачном/неудачном создании заказа"
        }

    systemContext order_system "C1" {
        include *
        autoLayout
        }

     # Диаграмма уровня C2 (Контейнеры)
    container order_system "C2" {
        include *
        autoLayout
    }

      # Диаграмма уровня C3 (Компоненты)
    component apiApplication "C3" {
        include *
        autoLayout
    }
}
}
  