import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import calendar
 
st.set_page_config(layout="wide")

d=pd.read_csv("cleaned_data6.csv")
d["Date"]=pd.to_datetime(d["Date"])

def load_top_startup(p):
    df=d[d["Date"].dt.year==p].groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).head()
    st.dataframe(df)

def year_analysis(p):
    df=d[d["Date"].dt.year == p].groupby(d["Date"].dt.month).agg({"Amount in cr":"sum","Startup":"count"}).reset_index()
    df.rename(columns={"Startup":"Count"},inplace=True)
    df["Month"]=df["Date"].apply(lambda x: calendar.month_name[int(x)])
    c1,c2=st.columns(2)
    with c1:
        fig=px.line(df,x="Month",y="Amount in cr",title="Monthly Investment",labels={"Date":"Month"})
        st.plotly_chart(fig)
    with c2:
        fig=px.bar(df,x="Month",y="Count",title="Number of Startups Invested Month on Month",labels={"Date":"Month","Startup":"Count"},text_auto=True)
        st.plotly_chart(fig)
    


def load_overall_details():
    st.title("OVERALL ANALYSIS")
    c1,c2=st.columns(2)
    with c1:
        total=round(d["Amount in cr"].sum())
        st.metric("Total Amount Invested In Indian Startup",str(total)+"CR")
        Max=sorted(d.groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).tolist(),reverse=True)[0]
        st.metric("Maximum Amount Invested",str(Max)+"CR")
        st.subheader("Top 10 Most Funded Indian Startup")
        st.dataframe(d.groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).reset_index().head(11))
        
    with c2:
        Med=round(d[d["Amount in cr"]!=0]["Amount in cr"].median())
        Mean=round(d[d["Amount in cr"]!=0]["Amount in cr"].mean())
        c1,c2,c3=st.columns(3)
        with c1:
            st.metric("Average Investment",str(Mean)+"CR")
        with c2:
            st.metric("Median Investment",str(Med)+"CR")
        with c3:
            n=d["Startup"].unique().size
            st.metric("Total Funded Startup",n)
        fig=px.box(d[d["Amount in cr"]!=0],x="Amount in cr",log_x=True,title="INVESTMENT DISTRIBUTION")
        st.plotly_chart(fig)
    c1,c2=st.columns(2)
    
    df=d.groupby(d["Date"].dt.year)["Amount in cr"].sum().reset_index()
    with c1:
        fig=px.line(df,x="Date",y="Amount in cr",title="YEAR-WISE-YEAR INVESTMENT IN INDIAN STARTUP")
        st.plotly_chart(fig)
    with c2:
        df=d.groupby(d["Date"].dt.year)["Amount in cr"].count().reset_index()
        fig=px.line(df,x="Date",y="Amount in cr",title=" NUMBER OF STARTUPS INVESTED IN YEAR-WISE-YEAR ",labels={"Amount in cr":"Count"})
        st.plotly_chart(fig)
        
    st.subheader("Month On Month Investment For Selected Year")
    p=st.selectbox("Selected Year",[2015,2016,2017,2018,2019,2020])
    year_analysis(p)
    c1,c2=st.columns(2)
    with c1:
        st.subheader("ROUND WISE FUNDING")
        df=d.groupby("Type")["Amount in cr"].sum().reset_index()
        fig=px.pie(df,values="Amount in cr",names="Type")
        st.plotly_chart(fig)
    with c2:
        st.subheader("CITY WISE FUNDING")
        df=d.groupby("City")["Amount in cr"].sum().reset_index()
        fig=px.pie(df,values="Amount in cr",names="City")
        st.plotly_chart(fig)
        st.write('''IN CITIES WHERE THERE IS 0 AMOUNT INVESTED INDICATES THAT AMOUNT WAS UNDISCLOSED''')
        
    c1,c2=st.columns(2)
    with c1:
        st.subheader("TOP INDIAN STARTUP OF EACH YEAR (IN TERMS OF INVESTMENT)")
        a=d[d["Date"].dt.year==2015].groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).head(5).reset_index().head(1)
        b=d[d["Date"].dt.year==2016].groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).head(5).reset_index().head(1)
        c=d[d["Date"].dt.year==2017].groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).head(5).reset_index().head(1)
        t=d[d["Date"].dt.year==2018].groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).head(5).reset_index().head(1)
        e=d[d["Date"].dt.year==2019].groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).head(5).reset_index().head(1)
        f=d[d["Date"].dt.year==2020].groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).head(5).reset_index().head(1)
        df=pd.concat((a,b,c,t,e,f))
        df["Year"]=[2015,2016,2017,2018,2019,2020]
        df.set_index("Year",inplace=True)
        st.dataframe(df)
    with c2:
        st.subheader("TOP FIVE STARTUPS OF EACH YEAR")
        p=st.selectbox("SELECT YEAR",[2015,2016,2018,2019,2020])
        load_top_startup(p)
    
    
    
    
    
def investor_detail(investor):
    st.header(investor)
    st.subheader("Recent Investments")
    st.dataframe(d[d["Investor"].str.contains(investor)].sort_values(by="Date",ascending=False).head(5))
    #finding bar chart
    big=d[d["Investor"].str.contains(investor)].groupby("Startup")["Amount in cr"].sum().head(5)
    big_df=big.reset_index().head(5)
    fig=px.bar(big_df,x="Startup",y="Amount in cr",title="BIGGEST INVESTMENT")
    st.subheader("Biggest Investment")
    st.dataframe(d[d["Investor"].str.contains(investor)].groupby("Startup")["Amount in cr"].sum().sort_values(ascending=False).head())
    st.plotly_chart(fig)
    st.subheader("General Investment Sector")
    c1,c2=st.columns(2)
    with c1:
        big=d[d["Investor"].str.contains(investor)].groupby("Industry Vertical")["Amount in cr"].sum().reset_index().sort_values("Amount in cr",ascending=False)[["Industry Vertical","Amount in cr"]].head(8)
        st.dataframe(big)
    with c2:
        plt.figure(figsize=(30,50))
        big=d[d["Investor"].str.contains(investor)]
        fig=px.sunburst(big,path=["Industry Vertical","Startup"],values="Amount in cr",width=1500,height=750,title="Sector->Startup")
        st.plotly_chart(fig)
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Stage Wise Investment")
        big=d[d["Investor"].str.contains(investor)].groupby("Type")["Amount in cr"].sum().reset_index()
        st.dataframe(big)
        fig=px.pie(big,values="Amount in cr",names="Type")
        st.plotly_chart(fig)
    with c2:
        st.subheader("City Wise Investment")
        big=d[d["Investor"].str.contains(investor)].groupby("City")["Amount in cr"].sum().reset_index()
        st.dataframe(big)
        fig=px.pie(big,values="Amount in cr",names="City")
        st.plotly_chart(fig)
    big=d[d["Investor"].str.contains(investor)]
    df=big.groupby(d["Date"].dt.year)["Amount in cr"].sum().reset_index()
    fig=px.line(df,x="Date",y="Amount in cr",title="YEAR-WISE-YEAR INVESTMENT")
    st.plotly_chart(fig)
    
    
def startup_detail(startup):
    st.title(startup)
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.metric("TOTAL AMOUNT INVESTED IN CR",d[d["Startup"]==startup]["Amount in cr"].sum())
    with c2:
        st.metric("AVERAGE AMOUNT INVESTED IN CR",d[d["Startup"]==startup]["Amount in cr"].mean())
    with c3:
        st.metric("MAXIMUM AMOUNT INVESTED IN CR",d[d["Startup"]==startup]["Amount in cr"].max())
    with c4:
        s=str(d[d["Startup"]==startup]["Industry Vertical"].head(1).values)
        a=s[2:len(s)-2]
        st.metric("INDUSTRY",a)
    df=d[d["Startup"]==startup].groupby(d["Date"].dt.year)["Amount in cr"].sum().sort_index().reset_index().rename(columns={"Date":"Year"})
    c1,c2=st.columns(2)
    with c1:
        st.subheader("YEAR WISE YEAR INVESTMENT IN ")
        st.dataframe(df)
        fig=px.line(df,x="Year",y="Amount in cr",title="YEAR-WISE-YEAR INVESTMENT")
        st.plotly_chart(fig)
    with c2:
        st.subheader("TOP INVESTORS OF SELECTED YEAR")
        year=st.selectbox("SELECT YEAR",[2015,2016,2017,2018,2019,2020])
        df=d[d["Startup"]==startup]
        df=df[df["Date"].dt.year==year].sort_values("Amount in cr",ascending=False).head(5)
        st.dataframe(df)
        st.subheader("NUMBER OF INVESTORS YEAR WISE")
        df=d[d["Startup"]==startup].groupby(d["Date"].dt.year)["Amount in cr"].count().reset_index().rename(columns={"Date":"Year","Amount in cr":"Counts"})
        fig=px.bar(df,x="Year",y="Counts")
        st.plotly_chart(fig)
    
    
    
    
    
    

st.sidebar.title("INDIAN STARTUP FUNDING")
option=st.sidebar.selectbox("SELECT ONE",["OVERALL ANALYSIS","STARTUP","INVESTOR"])

if option == "OVERALL ANALYSIS":
    load_overall_details()
elif option =="STARTUP":
    p=st.sidebar.selectbox("STARTUP",sorted(d["Startup"].unique()),key="selected_startup")
    
    st.title("STARTUP ANALYSIS")
    startup_detail(p)
        
else:
    st.title("INVESTOR ANALYSIS")
    investor=st.sidebar.selectbox("INVESTOR",sorted(set(d["Investor"].str.split(",").sum())))
    btn2=st.sidebar.button("SEARCH")
    if btn2:
        investor_detail(investor)
   
