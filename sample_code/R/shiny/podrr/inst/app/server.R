function(input, output, session) {
  ns <- session$ns
  values <- reactiveValues(tbl_name = '', tbl = data.frame())

  observeEvent(input$go, {
    errMsg <- shiny::reactive({shiny::validate(
      need(input$user != "", "Please enter a username."),
      need(input$password != "", "Please enter a password.")
    )})
    output$errMsg <- shiny::renderUI({
      errMsg()
    })
    req(input$user != "")
    req(input$password != "")

    con <- tryCatch(
      DBI::dbConnect(RPostgreSQL::PostgreSQL(),
                     host = "podr.phuse.global",
                     dbname = "nihpo",
                     user = input$user,
                     password = input$password,
                     port = 5432)
      , error = function(e) {
      output$errMsg <- shiny::renderUI({
        "Either username or password is incorrect"
      })
    })
    output$errMsg <- shiny::renderUI({
      "Select a table below:"
    })

    # Show buttons for all public tables
    alltables <- DBI::dbGetQuery(con,"SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    output$getTables <- renderUI({
      lapply(alltables$table_name, function(button){
        actionButton(button, button)
      })
    })

    # show preview of each table
    output$homepage <- renderUI({

      fluidRow(
        column(12, align = "center", h1("Table preview")),
        column(12, shinycssloaders::withSpinner(verbatimTextOutput("getTable")))
      )
    })
    output$getTable <- renderPrint({data.frame(Table = "Select a table from the sidebar...")})

    lapply(alltables$table_name, function(button){
          observeEvent(input[[button]], {

            values$tbl_name <- button
            output$getTable <- renderPrint({
              dplyr::as_tibble(DBI::dbGetQuery(con, glue::glue("SELECT * FROM {button} LIMIT 10")))
            })

            output$fetch <- renderUI({
              fluidRow(actionButton("fetchBttn", "Fetch a Specific Number of Rows"))
            })
            output$nrow <- renderUI({
              textInput(inputId = "nrow", label = "Number of rows to retreive", value = 10, placeholder = "Enter an integer.")
            })
            output$download <- renderUI({NULL})
          })
    })

    ## Fetch entire table
    observeEvent(input$fetchBttn, {
      nr <- as.numeric(input$nrow)
      if(nr != "" & is.numeric(nr)) {
        shiny::withProgress(message = paste0("Fetching: ", values$tbl_name),
                            detail = 'A download button will appear when ready...', value = 0, {
                              res <- DBI::dbSendQuery(con, glue::glue("SELECT * FROM {values$tbl_name} LIMIT {nr}"))
                              chunkList <- list()
                              while(!DBI::dbHasCompleted(res)){
                                incProgress(1/15)
                                chunk <- DBI::dbFetch(res, n = 25)
                                print(chunk)
                                print(as.character(nrow(chunk)))
                                chunkList <- rlist::list.append(chunkList, chunk)
                              }
                              DBI::dbClearResult(res)
                              values$tbl <- do.call(rbind, chunkList)
                            })
      } else {
        showModal(modalDialog(
          title = "Error",
          "Number of rows must be specified and should be an integer!",
          easyClose = TRUE
        ))
      }

      output$download <- renderUI({
        fluidRow(shinycssloaders::withSpinner(downloadButton("downloadData", "Download Table")))
      })

    })


    output$downloadData <- downloadHandler(
      filename = function() {
        paste(values$tbl_name, Sys.Date(), ".csv", sep="")
      },
      content = function(file) {
        shiny::withProgress(message = 'Download in progress',
                            detail = 'This may take a while...', value = 0, {

          write.csv(values$tbl, file)
        })
      }
    )

  })
}
