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

                authService = component "Auth_service" {
                    description "Регистрация и авторизация пользователей в роли заказчика или подрядчика"
                }

                securityService = component "Security_service" {
                    description "создание и выдача JWT в зависимости от роли, проверка JWT, добавление данных о регистрации пользователей в БД"
                }

                serviceComponent = component "Service_component" {
                    description "Предоставляет функционал для работы с услугами: получение списка услуг, создание новой услуги"
                } 
                
                orderingService = component "Ordering_service" {
                    description "Предоставляет функционал для работы с заказами покупателей: добавление услуг в заказ, получение заказа пользователя"
                } 

                orderingController = component "Ordering_controller" {
                    description "Контроллер для работы с таблицами заказов"
                } 

                servicesController = component "Services_controller" {
                    description "Контроллер для работы с таблицами услуг"
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
        orderingController -> Database "CRUD"
        servicesController -> Database "CRUD"
        authService -> securityService 
        securityService -> Database "CRUD"
        orderingService -> orderingController
        serviceComponent -> servicesController
        }

    views {
    themes default

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
  