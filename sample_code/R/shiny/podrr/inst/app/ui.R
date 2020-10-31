header <- shinydashboard::dashboardHeader(
  title = "PODRR"
)

# Sidebar
sidebar <- shinydashboard::dashboardSidebar(width = 400,
  textInput(inputId = "user", label = "Username", value = "", placeholder = "Enter username"),
  passwordInput(inputId = "password", label = "Password", value = "", placeholder = "Enter password"),
  actionButton("go", "Get Tables"),
  uiOutput("errMsg"),
  uiOutput("getTables")
)

## Body
body <- shinydashboard::dashboardBody(
    dashboardthemes::shinyDashboardThemes(
      theme = "grey_dark"
    ),
  fluidPage(
    uiOutput("nrow"),
    uiOutput("fetch"),
    uiOutput("download"),
    uiOutput("homepage")
  )
)


shinydashboard::dashboardPage(
  header,
  sidebar,
  body
)
