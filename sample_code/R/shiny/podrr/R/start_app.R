#' Start App
#'
#' @param ... passed to \link[shiny]{runApp}
#' @export
#' @rdname start shiny app
start_app <- function() {
  appDir <- system.file("/app", package = "podrr")
  shiny::runApp(appDir, launch.browser = TRUE)
}
