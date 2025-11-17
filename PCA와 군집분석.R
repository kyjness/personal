setwd("C:/Users/yujin/Desktop/캐글&데이콘/Global Energy and Emissions Dataset (1980–2021)")
master = read.csv("MASTER.csv")
master
str(master)
library(readxl)
global = read_excel("MASTER_GLOBAL.xlsx")
global


# 필요한 패키지 로드
library(dplyr)
library(readr)

# 수치형 변수만 추출 (분석용 컬럼)
#Temp Change는 "결과 변수"라서 빠짐짐
num_cols <- c("Total.CO2", "Coal.CO2", "Oil.CO2", "Gas.CO2", "Cement.CO2", "Flaring.CO2",
              "Other.CO2", "Per.Capita.CO2", "Total.Energy.Production", "Coal.Energy",
              "Gas.Energy", "Petroleum.and.other.liquids.Energy", "Nuclear.Energy",
              "Renewables.and.other.Energy", "CH4", "Population")

# 1. 과거 평균 (1980–2000)
past_avg <- master %>%
  filter(Year >= 1980 & Year <= 2000) %>%
  group_by(Country) %>%
  summarise(across(all_of(num_cols), ~mean(.x, na.rm = TRUE)), .groups = "drop") %>%
  rename_with(~ paste0(.x, "_past"), -Country)

# 2. 현재 평균 (2001–2021)
recent_avg <- master %>%
  filter(Year >= 2001 & Year <= 2021) %>%
  group_by(Country) %>%
  summarise(across(all_of(num_cols), ~mean(.x, na.rm = TRUE)), .groups = "drop") %>%
  rename_with(~ paste0(.x, "_recent"), -Country)

# 3. 변화량 = 최근 - 과거
# (중간 diff_df는 사용되지 않으므로 생략 가능)

change_df <- recent_avg %>%
  inner_join(past_avg, by = "Country") %>%
  mutate(across(ends_with("_recent"), 
                ~ .x - get(sub("_recent", "_past", cur_column())), 
                .names = "{gsub('_recent', '_diff', .col)}")) %>%
  select(Country, ends_with("_diff"))

# 4. 전체 평균 (1980–2021)
overall_avg <- master %>%
  filter(Year >= 1980 & Year <= 2021) %>%
  group_by(Country) %>%
  summarise(across(all_of(num_cols), ~mean(.x, na.rm = TRUE)), .groups = "drop") %>%
  rename_with(~ paste0(.x, "_mean"), -Country)


# 필요한 패키지 로드
library(tidyverse)
library(ggplot2)
library(factoextra)  # Scree plot 그리기에 유용
library(psych)       # loadings 보기 좋게 출력 가능


# 1.mean 데이터 행렬 준비
#전체평균
X <- overall_avg
X <- as.data.frame(X)
rownames(X) <- overall_avg$Country

#변화량
X <- change_df
X <- as.data.frame(X)
rownames(X) <- change_df$Country

# 2.상관행렬R 계산
X <- X %>% select(-Country) #범주형 컬럼인 country 제거
R <- round(cor(X), 3)
R

# 3 스펙트럼 분해
eigen.R <- eigen(R)
(eig_values = round(eigen.R$values, 3)) # 고유값
V=round(eigen.R$vectors, 3) # 고유벡터
V

#4.요인수 결정정
# 설명비율,누적 설명비율(%)
var_explained <- eig_values / sum(eig_values) * 100
round(var_explained,2)
cum_var_explained <- cumsum(var_explained)
round(cum_var_explained,2)

# 데이터프레임 준비
df_scree <- data.frame(
  PC = 1:length(eig_values),
  Eigenvalue = eig_values,
  CumulativeVar = cum_var_explained
)

# ggplot 으로 그리기
library(ggplot2)
ggplot(df_scree, aes(x = PC, y = Eigenvalue)) +
  geom_point(size = 5) +
  geom_line() +
  geom_hline(yintercept = 1, linetype = "dashed", color = "red") + 
  geom_text(aes(label = paste0("CPV=", round(CumulativeVar, 1), "%")),
            vjust = -0.5, size = 7) +  # CPV 표시
  scale_x_continuous(breaks = 1:nrow(df_scree)) +
  ylab("Eigenvalue") +
  theme_minimal()


# 5. 주성분 점수(PC Scores): 원래 변수들의 선형 결합
V2=V[,1:3]
V2

# 6.주성분 점수(PC Scores) 및 새로운 데이터 행렬 P 계산
# Y: 평균 중심화된 데이터 행렬 (평균 0으로 맞추기)
Y=scale(X, scale=T) # 중심화된 데이터 행렬
P=Y%*%V2            # P: 주성분 점수 행렬 (원본 데이터를 주성분 축으로 투영한 결과)
P

cor(P,Y) #음의 관계이므로 V2에 -붙일것을 추천
V2=-V2
rownames(V2) = colnames(Y)
colnames(V2) = c('PC1','PC2','PC3')
V2
P=Y%*%V2 #주성분점수 재정의
P
rownames(P) = change_df$Country
colnames(P) = c('PC1score','PC2score','PC3score')

# 7.주성분 점수(PC Scores) 시각화(Biplot)
pca_results <- prcomp(X, scale=TRUE)
fviz_pca_ind(pca_results, repel = TRUE)

# 7.주성분 점수(PC Scores)를 2차원에 시각화
par(pty="s")
lim<-range(pretty(P))
plot(P[,1], P[, 2], main="Plot of PCs Scores", xlim=lim, ylim=lim, 
     xlab="1st PC", ylab="2nd PC")
text(P[,1]+2, P[, 2], rownames(Y), cex=0.8, col="blue", pos=3)
abline(v=0, h=0)


#군집분석

# 불러오기
library(cluster)
library(factoextra)
library(ggplot2)
library(reshape2)

# 데이터 준비
X <- change_df %>% select(-Country)   # Country 제거
X <- scale(X) 



# clabel 함수: 군집 수 x일 때 kmeans 수행 후 cluster 결과(factor형) 반환
clabel = function(x) {
  factor(kmeans(x = X, centers = INTP.KM(dat = X, ncluster = x))$cluster)}

# from ~ to 범위까지 반복 → 각 군집 수별 cluster 결과 data frame으로 저장
# CNvalidity 함수를 이용해 군집 결과의 Validity(타당성) 평가 → 군집의 적절성 판단
from = 1;to = 11
clusters = data.frame(lapply(from:to, clabel))
names(clusters) = from:to
view(CNvalidity(dat = X, clusters = clusters))

# 군집 수 2~10까지 실루엣계수 계산
silhouette_scores <- c()
for (k in 2:10) {
  kmodel <- kmeans(X, centers = INTP.KM(dat = X, ncluster = k))
  sil <- silhouette(kmodel$cluster, dist(X))
  silhouette_scores[k] <- mean(sil[, 3])
}
silhouette_scores[2:10]

# 결과 저장용 벡터
sse_values <- c()
for (k in 2:10) {
  kmodel <- kmeans(X, centers = INTP.KM(dat = X, ncluster = k))
  sse_values[k] <- kmodel$tot.withinss
}
sse_values[2:10]

# 데이터프레임으로 정리
df <- data.frame(
  k = 2:10,
  SSE = sse_values[2:10],
  Silhouette = silhouette_scores[2:10])

# 시각화 (ggplot)
ggplot(df, aes(x = k)) +
  geom_line(aes(y = SSE, color = "SSE"), size = 1.2) +
  geom_point(aes(y = SSE, color = "SSE"), size = 2) +
  geom_line(aes(y = Silhouette * max(SSE), color = "Silhouette"), size = 1.2) +
  geom_point(aes(y = Silhouette * max(SSE), color = "Silhouette"), size = 2) +
  scale_y_continuous(
    name = "SSE",
    sec.axis = sec_axis(~ . / max(sse_values[2:10]), name = "Silhouette Score")
  ) +
  scale_color_manual(values = c("SSE" = "blue", "Silhouette" = "red")) +
  labs(
    x = "Number of Clusters",
    title = "Clustering Result (Elbow & Silhouette)"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5),
    legend.title = element_blank())

#군집수 4인 경우로 진행행
INTP = INTP.KM(dat = X, ncluster = 4)
kmeans_result = kmeans(x = X, centers = INTP)
kmeans_result

#변화량 주성분 점수 표
P_df = as.data.frame(P)
P_df$Country = rownames(P)
cluster_df = data.frame(Country = change_df$Country, 
                        Cluster = factor(kmeans_result$cluster))
merged_df = merge(P_df, cluster_df, by = "Country")
merged_df

# 군집별 국가명 리스트
country_list <- merged_df %>%
  group_by(Cluster) %>%
  summarise( mean_PC1 = mean(PC1),
             mean_PC2 = mean(PC2),
             mean_PC3 = mean(PC3),
             Countries = paste(Country, collapse = ", "))
country_list

# 7️⃣ Cluster별 PCA 점수 박스플롯 출력 (예: PC1~PC3)
library(ggplot2)

# PC1
ggplot(merged_df, aes(x = Cluster, y = PC1, fill = Cluster)) +
  geom_boxplot() +
  labs(title = "Cluster별 PC1 Score 분포",
       y = "PC1 Score") +
  theme_minimal()

# PC2
ggplot(merged_df, aes(x = Cluster, y = PC2, fill = Cluster)) +
  geom_boxplot() +
  labs(title = "Cluster별 PC2 Score 분포",
       y = "PC2 Score") +
  theme_minimal()

# PC3
ggplot(merged_df, aes(x = Cluster, y = PC3, fill = Cluster)) +
  geom_boxplot() +
  labs(title = "Cluster별 PC3 Score 분포",
       y = "PC3 Score") +
  theme_minimal()

# Cluster별 국가명 테이블 만들기 (지도용)
cluster_map_df <- merged_df %>%
  select(Country, Cluster)

library(rnaturalearth)
library(rnaturalearthdata)
library(sf)
library(ggplot2)
library(dplyr)
 
unique(merged_df$Country[grepl("United", merged_df$Country)])


# world map 데이터 (sf형)
world <- ne_countries(scale = "medium", returnclass = "sf")

# Country 이름 통일 (예: 미국)
merged_df$Country <- merged_df$Country %>%
  str_replace("United States", "United States of America")

# Cluster 열을 factor로 변환 (지도 색상 표시 위해)
merged_df$Cluster <- factor(merged_df$Cluster)

# world + Cluster merge
world_cluster <- world %>%
  left_join(merged_df, by = c("name" = "Country"))

# 지도 출력
ggplot(world_cluster) +
  geom_sf(aes(fill = Cluster), color = "gray70") +
  scale_fill_manual(values = c("1" = "#4B0000",
                               "2" = "#B22222",
                               "3" = "#FF7F50",
                               "4" = "#FFDAB9"),
                    na.value = "grey90") +   # NA 값 색상 설정
  theme_minimal() +
  labs(title = "World Map by Cluster",
       fill = "Cluster")

