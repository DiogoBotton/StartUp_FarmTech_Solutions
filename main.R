# Defina um espelho do CRAN e aumente o tempo limite de download
setup_environment <- function() {
  options(repos = c(CRAN = "https://cloud.r-project.org"))
  options(timeout = 120)
}

# Instale pacotes necessários
install_required_packages <- function() {
  required_packages <- c("httr", "ggplot2", "jsonlite", "readr", "gridExtra",
                         "bit", "prettyunits", "bit64", "tidyselect", "progress",
                         "clipr", "crayon", "hms", "vroom", "cpp11", "tzdb")

  install_if_missing <- function(pkg) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      tryCatch({
        install.packages(pkg, dependencies = TRUE)
      }, error = function(e) {
        message(paste("Erro ao instalar o pacote", pkg, ":", e$message))
      })
    }
  }

  invisible(lapply(required_packages, install_if_missing))
  lapply(required_packages, library, character.only = TRUE)
}

# Defina as coordenadas das capitais dos estados do Brasil
define_cities <- function() {
  list(
    "Rio Branco" = c(-9.974, -67.8076),
    "Maceió" = c(-9.6658, -35.735),
    "Macapá" = c(0.0349, -51.0694),
    "Manaus" = c(-3.1019, -60.025),
    "Salvador" = c(-12.9714, -38.5014),
    "Fortaleza" = c(-3.7172, -38.5434),
    "Brasília" = c(-15.7801, -47.9292),
    "Vitória" = c(-20.3155, -40.3128),
    "Goiânia" = c(-16.6869, -49.2648),
    "São Luís" = c(-2.5307, -44.3068),
    "Cuiabá" = c(-15.601, -56.0974),
    "Campo Grande" = c(-20.4697, -54.6201),
    "Belo Horizonte" = c(-19.9208, -43.9378),
    "Belém" = c(-1.4558, -48.4902),
    "João Pessoa" = c(-7.115, -34.8631),
    "Curitiba" = c(-25.4284, -49.2733),
    "Recife" = c(-8.0476, -34.877),
    "Teresina" = c(-5.0892, -42.8019),
    "Rio de Janeiro" = c(-22.9068, -43.1729),
    "Natal" = c(-5.7945, -35.211),
    "Porto Alegre" = c(-30.0346, -51.2177),
    "Porto Velho" = c(-8.7612, -63.9039),
    "Boa Vista" = c(2.819, -60.6733),
    "Florianópolis" = c(-27.5954, -48.548),
    "São Paulo" = c(-23.5505, -46.6333),
    "Aracaju" = c(-10.9472, -37.0731),
    "Palmas" = c(-10.1842, -48.3336)
  )
}

# Faça a requisição para cada cidade
fetch_weather_data <- function(cities, base_url, start_date, end_date) {
  data <- list()

  for (city in names(cities)) {
    coords <- cities[[city]]
    url <- paste0(base_url, "?latitude=", coords[1], "&longitude=", coords[2], "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&start_date=", start_date, "&end_date=", end_date, "&format=json")
    response <- GET(url)
    if (status_code(response) == 200) {
      content <- fromJSON(content(response, "text", encoding = "UTF-8"))
      if (!is.null(content$daily)) {
        data[[city]] <- data.frame(
          city = city,
          date = as.Date(content$daily$time),
          temp_max = content$daily$temperature_2m_max,
          temp_min = content$daily$temperature_2m_min,
          precipitation = content$daily$precipitation_sum
        )
      }
    } else {
      print(paste("Erro na requisição para", city, ":", status_code(response)))
      print(paste("URL:", url))
      print(content(response, "text", encoding = "UTF-8"))
    }
  }

  data
}

# Combine os dados em um único data frame
combine_data <- function(data) {
  if (length(data) > 0) {
    data_df <- do.call(rbind, data)
    data_df$date <- as.Date(data_df$date)
    data_df$year <- format(data_df$date, "%Y")
    data_df
  } else {
    NULL
  }
}

# Calcular a soma anual de precipitação para cada cidade
calculate_annual_precipitation <- function(data_df) {
  aggregate(precipitation ~ city + year, data = data_df, sum)
}

# Calcular a média mensal de precipitação para cada cidade
calculate_monthly_precipitation <- function(annual_precipitation) {
  aggregate(precipitation ~ city, data = annual_precipitation, function(x) mean(x) / 12)
}

# Calcular a média anual de temperatura mínima e máxima para cada cidade
calculate_annual_temperature <- function(data_df) {
  aggregate(cbind(temp_min, temp_max) ~ city, data = data_df, mean)
}

# Leia a lista de cultivos do arquivo CSV
read_cultivos <- function(file_path) {
  read_csv(file_path)
}

# Recomendar cultivos com base na soma anual de precipitação e temperatura
recommend_crops <- function(annual_precipitation, annual_temperature, cultivos) {
  recommendations <- list()

  for (i in 1:nrow(annual_precipitation)) {
    state <- annual_precipitation$city[i]
    precip_sum <- annual_precipitation$precipitation[i]
    temp_min <- annual_temperature$temp_min[annual_temperature$city == state]
    temp_max <- annual_temperature$temp_max[annual_temperature$city == state]

    recommended_crops <- cultivos[
      cultivos$`Índice Hídrico Anual Recomendado Mínimo (mm)` <= precip_sum &
      cultivos$`Índice Hídrico Anual Recomendado Máximo (mm)` >= precip_sum &
      cultivos$`Temperatura Mínima (°C)` <= temp_min &
      cultivos$`Temperatura Máxima (°C)` >= temp_max,
      "Cultivo"
    ]

    recommendations[[state]] <- recommended_crops
  }

  recommendations
}

# Plotar o gráfico de barras com a soma absoluta da precipitação e os pontos de média mensal conectados
plot_precipitation_graph <- function(annual_precipitation, monthly_precipitation) {
  ggplot(annual_precipitation, aes(x = city, y = precipitation, fill = "Soma Anual")) +
    geom_bar(stat = "identity") +
    geom_point(data = monthly_precipitation, aes(x = city, y = precipitation, color = "Média Mensal"), size = 3) +
    geom_line(data = monthly_precipitation, aes(x = city, y = precipitation, group = 1, color = "Média Mensal"), linetype = "solid", linewidth = 1) +
    scale_fill_manual(name = "Legenda", values = c("Soma Anual" = "lightgreen")) +
    scale_color_manual(name = "Legenda", values = c("Média Mensal" = "blue")) +
    theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
    labs(title = "Soma Anual de Precipitação nas Capitais dos Estados do Brasil (Último Ano)", x = "Cidade", y = "Precipitação (mm)")
}

# Salvar o gráfico em PDF com boa resolução
save_graph <- function(graph, file_path) {
  ggsave(file_path, plot = graph, width = 16, height = 9, limitsize = FALSE)
}

# Criar uma tabela com as recomendações
create_recommendations_table <- function(recommendations) {
  do.call(rbind, lapply(names(recommendations), function(state) {
    data.frame(Estado = state, Cultivos = paste(recommendations[[state]], collapse = ", "))
  }))
}

# Salvar a tabela em PDF com boa resolução
save_table <- function(table, file_path) {
  pdf(file_path, width = 16, height = 9)
  grid.table(table)
  dev.off()
}

# Função principal
main <- function() {
  setup_environment()
  install_required_packages()

  cities <- define_cities()
  base_url <- "https://api.open-meteo.com/v1/forecast"
  end_date <- Sys.Date()
  start_date <- end_date - 365
  max_end_date <- as.Date("2024-09-25")
  if (end_date > max_end_date) {
    end_date <- max_end_date
  }

  data <- fetch_weather_data(cities, base_url, start_date, end_date)
  data_df <- combine_data(data)

  if (!is.null(data_df)) {
    annual_precipitation <- calculate_annual_precipitation(data_df)
    monthly_precipitation <- calculate_monthly_precipitation(annual_precipitation)
    annual_temperature <- calculate_annual_temperature(data_df)
    cultivos <- read_cultivos("cultivos.csv")
    recommendations <- recommend_crops(annual_precipitation, annual_temperature, cultivos)

    graph <- plot_precipitation_graph(annual_precipitation, monthly_precipitation)
    save_graph(graph, file.path(getwd(), "grafico_precipitacao.pdf"))

    recommendations_table <- create_recommendations_table(recommendations)
    save_table(recommendations_table, file.path(getwd(), "tabela_recomendacoes.pdf"))

    print(paste("Gráfico de precipitação salvo em", file.path(getwd(), "grafico_precipitacao.pdf")))
    print(paste("Tabela de recomendações salva em", file.path(getwd(), "tabela_recomendacoes.pdf")))
  } else {
    print("Nenhum dado foi recuperado das requisições.")
  }
}

# Execute a função principal
main()