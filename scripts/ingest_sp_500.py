#https://www.slickcharts.com/sp500
from pathlib import Path

RAW = '''# 	Company 	Symbol 	Weight 	      Price 	Chg 	% Chg
1 	Apple Inc 	AAPL 	7.427244 	  185.20 	0.28 	(0.15%)
2 	Microsoft Corp 	MSFT 	6.914768 	  338.13 	-4.20 	(-1.23%)
3 	Amazon.com Inc 	AMZN 	3.043082 	  125.81 	0.32 	(0.25%)
4 	Nvidia Corp 	NVDA 	2.868252 	  438.73 	11.81 	(2.77%)
5 	Alphabet Inc Cl A 	GOOGL 	1.993679 	  123.22 	-0.31 	(-0.25%)
6 	Tesla Inc 	TSLA 	1.906815 	  274.64 	14.10 	(5.41%)
7 	Alphabet Inc Cl C 	GOOG 	1.722297 	  123.95 	-0.11 	(-0.09%)
8 	Meta Platforms Inc Class A 	META 	1.688671 	  284.16 	3.16 	(1.12%)
9 	Berkshire Hathaway Inc Cl B 	BRK.B 	1.63893 	  338.83 	0.52 	(0.15%)
10 	Unitedhealth Group Inc 	UNH 	1.159627 	  469.99 	11.50 	(2.51%)
11 	Johnson & Johnson 	JNJ 	1.159413 	  164.45 	0.22 	(0.14%)
12 	Exxon Mobil Corp 	XOM 	1.154659 	  102.86 	-2.27 	(-2.16%)
13 	Jpmorgan Chase & Co 	JPM 	1.13729 	  142.56 	-0.70 	(-0.49%)
14 	Visa Inc Class a Shares 	V 	1.006297 	  226.46 	-2.45 	(-1.07%)
15 	Broadcom Inc 	AVGO 	0.984327 	  868.31 	0.20 	(0.02%)
16 	Eli Lilly & Co 	LLY 	0.958044 	  451.79 	4.08 	(0.91%)
17 	Procter & Gamble Co 	PG 	0.957216 	  148.30 	-1.24 	(-0.83%)
18 	Mastercard Inc A 	MA 	0.855898 	  374.53 	-2.00 	(-0.53%)
19 	Home Depot Inc 	HD 	0.826342 	  301.70 	1.32 	(0.44%)
20 	Merck & Co. Inc. 	MRK 	0.75356 	  110.47 	1.15 	(1.05%)
21 	Chevron Corp 	CVX 	0.744491 	  153.71 	-3.55 	(-2.26%)
22 	Pepsico Inc 	PEP 	0.695207 	  185.34 	-0.70 	(-0.38%)
23 	Abbvie Inc 	ABBV 	0.665252 	  137.88 	-0.76 	(-0.55%)
24 	Coca Cola Co 	KO 	0.651256 	  61.25 	-0.42 	(-0.68%)
25 	Costco Wholesale Corp 	COST 	0.630444 	  519.65 	-4.00 	(-0.76%)
26 	Adobe Inc 	ADBE 	0.617044 	  486.23 	-8.95 	(-1.81%)
27 	Pfizer Inc 	PFE 	0.614358 	  39.41 	-0.65 	(-1.63%)
28 	Walmart Inc 	WMT 	0.591781 	  154.29 	-1.25 	(-0.80%)
29 	Mcdonald S Corp 	MCD 	0.583664 	  293.11 	-0.59 	(-0.20%)
30 	Cisco Systems Inc 	CSCO 	0.580405 	  51.59 	-0.49 	(-0.93%)
31 	Salesforce Inc 	CRM 	0.563198 	  216.85 	5.09 	(2.40%)
32 	Thermo Fisher Scientific Inc 	TMO 	0.563003 	  527.63 	-9.67 	(-1.80%)
33 	Bank of America Corp 	BAC 	0.549779 	  28.93 	-0.27 	(-0.91%)
34 	Accenture Plc Cl A 	ACN 	0.548206 	  318.06 	-1.48 	(-0.46%)
35 	Advanced Micro Devices 	AMD 	0.525324 	  118.81 	-1.27 	(-1.06%)
36 	Oracle Corp 	ORCL 	0.524487 	  122.02 	-3.44 	(-2.74%)
37 	Netflix Inc 	NFLX 	0.521958 	  434.27 	2.31 	(0.53%)
38 	Abbott Laboratories 	ABT 	0.502432 	  106.83 	0.63 	(0.60%)
39 	Linde Plc 	LIN 	0.499148 	  368.98 	-6.31 	(-1.68%)
40 	Comcast Corp Class A 	CMCSA 	0.465531 	  40.65 	-0.56 	(-1.35%)
41 	Walt Disney Co 	DIS 	0.452643 	  89.93 	-1.39 	(-1.53%)
42 	Danaher Corp 	DHR 	0.436234 	  236.94 	-4.86 	(-2.01%)
43 	Texas Instruments Inc 	TXN 	0.434527 	  174.30 	-2.46 	(-1.39%)
44 	Wells Fargo & Co 	WFC 	0.429951 	  41.87 	-0.32 	(-0.75%)
45 	Nextera Energy Inc 	NEE 	0.415502 	  74.70 	-0.90 	(-1.18%)
46 	Verizon Communications Inc 	VZ 	0.415486 	  35.83 	-0.64 	(-1.74%)
47 	Intel Corp 	INTC 	0.412104 	  34.96 	-1.41 	(-3.87%)
48 	Philip Morris International 	PM 	0.399127 	  94.87 	-0.02 	(-0.03%)
49 	Raytheon Technologies Corp 	RTX 	0.388515 	  97.80 	0.06 	(0.06%)
50 	Nike Inc Cl B 	NKE 	0.380194 	  109.61 	-3.98 	(-3.50%)
51 	Bristol Myers Squibb Co 	BMY 	0.377584 	  66.14 	-0.02 	(-0.03%)
52 	Qualcomm Inc 	QCOM 	0.37108 	  119.86 	-2.82 	(-2.30%)
53 	Honeywell International Inc 	HON 	0.367962 	  200.39 	-2.58 	(-1.27%)
54 	S&p Global Inc 	SPGI 	0.353013 	  391.59 	-3.62 	(-0.92%)
55 	Lowe S Cos Inc 	LOW 	0.351681 	  215.59 	-1.49 	(-0.68%)
56 	United Parcel Service Cl B 	UPS 	0.351611 	  177.52 	-1.06 	(-0.60%)
57 	Intuit Inc 	INTU 	0.347412 	  455.22 	0.19 	(0.04%)
58 	Conocophillips 	COP 	0.344897 	  102.15 	-2.78 	(-2.64%)
59 	Caterpillar Inc 	CAT 	0.34338 	  241.56 	-3.71 	(-1.51%)
60 	Union Pacific Corp 	UNP 	0.339786 	  201.68 	-2.99 	(-1.46%)
61 	Intl Business Machines Corp 	IBM 	0.339133 	  136.04 	-1.44 	(-1.05%)
62 	Boeing Co 	BA 	0.337954 	  212.69 	-7.30 	(-3.32%)
63 	Amgen Inc 	AMGN 	0.332738 	  228.87 	-0.79 	(-0.35%)
64 	Medtronic Plc 	MDT 	0.321756 	  89.01 	-0.14 	(-0.16%)
65 	Applied Materials Inc 	AMAT 	0.317804 	  138.53 	-0.40 	(-0.29%)
66 	Starbucks Corp 	SBUX 	0.317684 	  101.28 	-0.59 	(-0.58%)
67 	General Electric Co 	GE 	0.313629 	  104.24 	-2.05 	(-1.93%)
68 	Intuitive Surgical Inc 	ISRG 	0.31314 	  327.60 	-1.76 	(-0.53%)
69 	Servicenow Inc 	NOW 	0.312973 	  559.75 	-5.73 	(-1.01%)
70 	Morgan Stanley 	MS 	0.312274 	  86.86 	-1.23 	(-1.40%)
71 	At&t Inc 	T 	0.310608 	  15.80 	-0.27 	(-1.65%)
72 	Prologis Inc 	PLD 	0.306662 	  120.86 	-1.77 	(-1.45%)
73 	Goldman Sachs Group Inc 	GS 	0.305537 	  330.99 	-7.32 	(-2.16%)
74 	Deere & Co 	DE 	0.299088 	  408.48 	0.85 	(0.21%)
75 	Blackrock Inc 	BLK 	0.286025 	  690.57 	-12.20 	(-1.74%)
76 	Elevance Health Inc 	ELV 	0.285423 	  439.29 	-3.92 	(-0.88%)
77 	Lockheed Martin Corp 	LMT 	0.281153 	  459.11 	-0.06 	(-0.01%)
78 	American Express Co 	AXP 	0.278071 	  169.57 	-2.64 	(-1.53%)
79 	Mondelez International Inc A 	MDLZ 	0.272201 	  73.28 	-0.29 	(-0.39%)
81 	Stryker Corp 	SYK 	0.269277 	  298.25 	3.90 	(1.32%)
82 	Gilead Sciences Inc 	GILD 	0.266825 	  77.82 	-1.04 	(-1.32%)
83 	Booking Holdings Inc 	BKNG 	0.26498 	  2,631.77 	-9.22 	(-0.35%)
84 	Analog Devices Inc 	ADI 	0.259046 	  188.08 	-0.29 	(-0.15%)
85 	Citigroup Inc 	C 	0.254854 	  47.67 	-0.52 	(-1.07%)
86 	Tjx Companies Inc 	TJX 	0.254724 	  80.48 	-0.78 	(-0.96%)
87 	Automatic Data Processing 	ADP 	0.24883 	  220.42 	-0.90 	(-0.41%)
88 	Marsh & Mclennan Cos 	MMC 	0.243387 	  181.17 	0.02 	(0.01%)
89 	American Tower Corp 	AMT 	0.243298 	  190.41 	-2.48 	(-1.29%)
90 	Vertex Pharmaceuticals Inc 	VRTX 	0.242668 	  342.78 	-5.11 	(-1.47%)
91 	Cvs Health Corp 	CVS 	0.235951 	  68.76 	1.04 	(1.53%)
92 	Regeneron Pharmaceuticals 	REGN 	0.228405 	  781.25 	-1.80 	(-0.23%)
93 	Lam Research Corp 	LRCX 	0.224287 	  614.81 	2.16 	(0.35%)
94 	Schwab (Charles) Corp 	SCHW 	0.219616 	  54.05 	-0.35 	(-0.65%)
95 	Chubb Ltd 	CB 	0.219167 	  193.39 	-1.55 	(-0.79%)
96 	The Cigna Group 	CI 	0.216079 	  270.67 	1.84 	(0.68%)
97 	Zoetis Inc 	ZTS 	0.215573 	  169.10 	-1.64 	(-0.96%)
98 	Altria Group Inc 	MO 	0.213473 	  43.53 	-0.55 	(-1.24%)
99 	Boston Scientific Corp 	BSX 	0.212153 	  53.98 	-0.35 	(-0.64%)
100 	Southern Co 	SO 	0.211625 	  70.34 	-1.42 	(-1.98%)
101 	Eaton Corp Plc 	ETN 	0.206388 	  194.55 	3.29 	(1.72%)
102 	Progressive Corp 	PGR 	0.206029 	  129.70 	-0.29 	(-0.23%)
103 	T Mobile Us Inc 	TMUS 	0.204853 	  131.27 	0.34 	(0.26%)
104 	Palo Alto Networks Inc 	PANW 	0.202664 	  241.79 	-4.74 	(-1.92%)
105 	Paypal Holdings Inc 	PYPL 	0.201345 	  68.94 	2.51 	(3.77%)
106 	Fiserv Inc 	FI 	0.201171 	  119.53 	-0.43 	(-0.36%)
107 	Micron Technology Inc 	MU 	0.200321 	  66.87 	-0.79 	(-1.17%)
108 	Becton Dickinson and Co 	BDX 	0.199087 	  256.82 	-1.81 	(-0.70%)
109 	Equinix Inc 	EQIX 	0.197811 	  779.87 	1.26 	(0.16%)
110 	Duke Energy Corp 	DUK 	0.192307 	  91.00 	-1.18 	(-1.28%)
111 	Illinois Tool Works 	ITW 	0.186756 	  244.04 	-3.95 	(-1.59%)
112 	Schlumberger Ltd 	SLB 	0.184115 	  47.29 	-0.49 	(-1.03%)
113 	Aon Plc Class A 	AON 	0.183524 	  329.04 	-0.34 	(-0.10%)
114 	Csx Corp 	CSX 	0.183418 	  32.93 	-0.29 	(-0.86%)
115 	Synopsys Inc 	SNPS 	0.182464 	  434.14 	-7.05 	(-1.60%)
116 	Eog Resources Inc 	EOG 	0.180447 	  110.34 	-3.08 	(-2.71%)
117 	Cme Group Inc 	CME 	0.179413 	  183.03 	-1.08 	(-0.59%)
118 	Northrop Grumman Corp 	NOC 	0.178908 	  454.28 	-4.08 	(-0.89%)
119 	Colgate Palmolive Co 	CL 	0.176271 	  77.70 	-0.08 	(-0.10%)
120 	Air Products & Chemicals Inc 	APD 	0.176152 	  289.80 	-3.37 	(-1.15%)
121 	Cadence Design Sys Inc 	CDNS 	0.175531 	  232.21 	-3.63 	(-1.54%)
122 	Kla Corp 	KLAC 	0.174657 	  464.88 	-0.01 	(-0.00%)
123 	Intercontinental Exchange In 	ICE 	0.169344 	  112.16 	0.48 	(0.43%)
124 	Target Corp 	TGT 	0.166831 	  132.64 	-1.17 	(-0.87%)
125 	Waste Management Inc 	WM 	0.166245 	  165.17 	0.14 	(0.09%)
126 	Hca Healthcare Inc 	HCA 	0.162583 	  285.47 	-4.61 	(-1.59%)
127 	Sherwin Williams Co 	SHW 	0.158599 	  248.76 	0.87 	(0.35%)
128 	Activision Blizzard Inc 	ATVI 	0.158395 	  81.92 	-0.06 	(-0.07%)
129 	3m Co W/d 	MMM 	0.156527 	  102.40 	-2.14 	(-2.05%)
130 	Freeport Mcmoran Inc 	FCX 	0.1547 	  39.40 	-0.50 	(-1.24%)
131 	Ford Motor Co 	F 	0.153706 	  14.23 	-0.19 	(-1.30%)
132 	Chipotle Mexican Grill Inc 	CMG 	0.152277 	  2,053.25 	20.33 	(1.00%)
133 	O Reilly Automotive Inc 	ORLY 	0.151987 	  916.45 	-2.57 	(-0.28%)
134 	Edwards Lifesciences Corp 	EW 	0.15141 	  91.94 	-0.00 	(-0.00%)
135 	Humana Inc 	HUM 	0.151098 	  447.26 	1.61 	(0.36%)
136 	Mckesson Corp 	MCK 	0.150948 	  410.65 	4.45 	(1.10%)
137 	Fedex Corp 	FDX 	0.147087 	  231.90 	-1.56 	(-0.67%)
138 	Moody S Corp 	MCO 	0.145597 	  340.44 	-1.41 	(-0.41%)
139 	General Motors Co 	GM 	0.143646 	  37.36 	-0.61 	(-1.59%)
140 	Pnc Financial Services Group 	PNC 	0.140356 	  126.77 	-1.70 	(-1.32%)
141 	Nxp Semiconductors Nv 	NXPI 	0.138869 	  195.44 	-2.41 	(-1.22%)
142 	Norfolk Southern Corp 	NSC 	0.138536 	  220.36 	-3.78 	(-1.69%)
143 	Dexcom Inc 	DXCM 	0.136126 	  129.99 	-0.11 	(-0.09%)
144 	Emerson Electric Co 	EMR 	0.135508 	  86.96 	-0.45 	(-0.52%)
145 	Crown Castle Inc 	CCI 	0.134434 	  112.64 	-1.97 	(-1.72%)
146 	General Dynamics Corp 	GD 	0.132706 	  215.56 	-1.78 	(-0.82%)
147 	Amphenol Corp Cl A 	APH 	0.132435 	  81.05 	-1.10 	(-1.34%)
148 	Roper Technologies Inc 	ROP 	0.131804 	  455.52 	-3.26 	(-0.71%)
149 	Pioneer Natural Resources Co 	PXD 	0.131313 	  202.11 	-4.69 	(-2.27%)
150 	Marathon Petroleum Corp 	MPC 	0.130579 	  111.23 	-2.07 	(-1.82%)
151 	General Mills Inc 	GIS 	0.129095 	  80.69 	-0.02 	(-0.02%)
152 	Parker Hannifin Corp 	PH 	0.128445 	  372.49 	3.39 	(0.92%)
153 	Estee Lauder Companies Cl A 	EL 	0.128205 	  197.86 	-6.09 	(-2.98%)
154 	Fortinet Inc 	FTNT 	0.127826 	  71.68 	-1.10 	(-1.51%)
155 	Motorola Solutions Inc 	MSI 	0.127153 	  278.88 	-1.37 	(-0.49%)
156 	Microchip Technology Inc 	MCHP 	0.127081 	  84.41 	-1.08 	(-1.26%)
157 	Us Bancorp 	USB 	0.126449 	  33.65 	0.20 	(0.59%)
158 	Sempra Energy 	SRE 	0.126198 	  147.43 	-0.77 	(-0.52%)
159 	Kimberly Clark Corp 	KMB 	0.126083 	  136.51 	-1.17 	(-0.85%)
160 	Autodesk Inc 	ADSK 	0.1251 	  212.11 	-1.39 	(-0.65%)
161 	Autozone Inc 	AZO 	0.124666 	  2,455.59 	-38.20 	(-1.53%)
162 	Arthur J Gallagher & Co 	AJG 	0.124398 	  211.54 	-2.24 	(-1.05%)
163 	Marriott International Cl A 	MAR 	0.123534 	  173.81 	-2.55 	(-1.45%)
164 	Public Storage 	PSA 	0.123136 	  285.58 	-1.52 	(-0.53%)
165 	Ecolab Inc 	ECL 	0.122402 	  180.67 	-1.37 	(-0.75%)
166 	Johnson Controls Internation 	JCI 	0.121719 	  65.77 	0.30 	(0.46%)
167 	Phillips 66 	PSX 	0.121075 	  93.59 	-3.54 	(-3.64%)
168 	Monster Beverage Corp 	MNST 	0.120599 	  58.37 	-0.09 	(-0.15%)
169 	Dominion Energy Inc 	D 	0.120573 	  53.18 	-0.16 	(-0.29%)
170 	American Electric Power 	AEP 	0.118216 	  84.47 	-0.46 	(-0.54%)
171 	Te Connectivity Ltd 	TEL 	0.117123 	  135.47 	-0.18 	(-0.13%)
172 	Trane Technologies Plc 	TT 	0.116676 	  185.75 	-1.31 	(-0.70%)
173 	Biogen Inc 	BIIB 	0.116392 	  293.96 	-3.52 	(-1.18%)
174 	Moderna Inc 	MRNA 	0.115201 	  124.10 	-4.63 	(-3.60%)
175 	Cintas Corp 	CTAS 	0.115138 	  484.28 	-7.08 	(-1.44%)
176 	Transdigm Group Inc 	TDG 	0.114824 	  820.70 	4.81 	(0.59%)
177 	Truist Financial Corp 	TFC 	0.11465 	  31.41 	-0.50 	(-1.55%)
178 	Occidental Petroleum Corp 	OXY 	0.114538 	  57.25 	-0.90 	(-1.55%)
179 	Capital One Financial Corp 	COF 	0.114059 	  109.28 	-0.79 	(-0.72%)
180 	American International Group 	AIG 	0.112659 	  56.16 	-1.14 	(-1.99%)
181 	Archer Daniels Midland Co 	ADM 	0.11232 	  74.14 	-1.34 	(-1.77%)
182 	Realty Income Corp 	O 	0.112274 	  60.35 	-1.05 	(-1.70%)
183 	Valero Energy Corp 	VLO 	0.112164 	  111.20 	-3.01 	(-2.63%)
184 	Paccar Inc 	PCAR 	0.111122 	  77.78 	-0.85 	(-1.09%)
185 	Exelon Corp 	EXC 	0.111116 	  40.75 	-0.47 	(-1.13%)
186 	Corteva Inc 	CTVA 	0.110916 	  56.63 	-0.61 	(-1.06%)
187 	Travelers Cos Inc 	TRV 	0.110838 	  175.46 	-1.29 	(-0.73%)
188 	Iqvia Holdings Inc 	IQV 	0.108716 	  214.90 	-1.12 	(-0.52%)
189 	Idexx Laboratories Inc 	IDXX 	0.108581 	  482.70 	-0.33 	(-0.07%)
190 	Welltower Inc 	WELL 	0.108572 	  79.36 	-1.05 	(-1.30%)
191 	Constellation Brands Inc A 	STZ 	0.108159 	  243.95 	-2.08 	(-0.84%)
192 	Carrier Global Corp 	CARR 	0.106517 	  47.54 	0.66 	(1.40%)
193 	Arista Networks Inc 	ANET 	0.105951 	  154.77 	-3.02 	(-1.91%)
194 	Yum Brands Inc 	YUM 	0.105724 	  135.95 	-2.63 	(-1.90%)
195 	On Semiconductor 	ON 	0.105417 	  89.48 	-0.67 	(-0.75%)
196 	Hershey Co 	HSY 	0.103978 	  258.13 	-2.59 	(-0.99%)
197 	Nucor Corp 	NUE 	0.103945 	  149.53 	-1.88 	(-1.24%)
198 	Aflac Inc 	AFL 	0.103707 	  67.88 	-1.55 	(-2.24%)
199 	Msci Inc 	MSCI 	0.103511 	  473.54 	-4.19 	(-0.88%)
200 	Hess Corp 	HES 	0.102058 	  132.32 	-3.24 	(-2.39%)
201 	Hilton Worldwide Holdings In 	HLT 	0.101807 	  139.75 	-1.06 	(-0.76%)
202 	Dow Inc 	DOW 	0.101339 	  51.94 	-1.22 	(-2.30%)
203 	Copart Inc 	CPRT 	0.101321 	  87.87 	0.59 	(0.67%)
204 	L3harris Technologies Inc 	LHX 	0.100936 	  195.59 	0.02 	(0.01%)
205 	Sysco Corp 	SYY 	0.100935 	  72.53 	-0.86 	(-1.17%)
206 	Ross Stores Inc 	ROST 	0.100745 	  107.30 	-0.55 	(-0.51%)
207 	Williams Cos Inc 	WMB 	0.100426 	  30.63 	0.10 	(0.31%)
208 	Otis Worldwide Corp 	OTIS 	0.10041 	  87.14 	-1.48 	(-1.68%)
209 	Simon Property Group Inc 	SPG 	0.10006 	  110.70 	-2.09 	(-1.86%)
210 	Paychex Inc 	PAYX 	0.098701 	  112.24 	-1.35 	(-1.19%)
211 	Dr Horton Inc 	DHI 	0.098684 	  118.26 	1.86 	(1.60%)
212 	Centene Corp 	CNC 	0.098121 	  66.06 	0.40 	(0.61%)
213 	Rockwell Automation Inc 	ROK 	0.097951 	  315.93 	0.13 	(0.04%)
214 	Dollar General Corp 	DG 	0.097807 	  164.93 	0.61 	(0.37%)
215 	Charter Communications Inc A 	CHTR 	0.097535 	  331.91 	-9.33 	(-2.73%)
216 	Ametek Inc 	AME 	0.097155 	  155.53 	-0.38 	(-0.24%)
217 	Agilent Technologies Inc 	A 	0.097131 	  118.06 	-3.07 	(-2.53%)
218 	Metlife Inc 	MET 	0.096989 	  54.48 	-1.02 	(-1.85%)
219 	Xcel Energy Inc 	XEL 	0.094751 	  63.02 	-0.90 	(-1.40%)
220 	Newmont Corp 	NEM 	0.094396 	  43.22 	-0.62 	(-1.40%)
221 	Ameriprise Financial Inc 	AMP 	0.092817 	  322.37 	-2.63 	(-0.81%)
222 	Costar Group Inc 	CSGP 	0.092699 	  85.35 	1.21 	(1.44%)
223 	Kinder Morgan Inc 	KMI 	0.0912 	  16.69 	-0.36 	(-2.08%)
224 	Electronic Arts Inc 	EA 	0.090926 	  126.36 	-2.30 	(-1.79%)
225 	Ppg Industries Inc 	PPG 	0.090784 	  142.40 	-0.68 	(-0.47%)
226 	Cummins Inc 	CMI 	0.090404 	  233.41 	-2.40 	(-1.02%)
227 	Cognizant Tech Solutions A 	CTSH 	0.089864 	  64.73 	-0.36 	(-0.55%)
228 	Ww Grainger Inc 	GWW 	0.089533 	  732.01 	-0.42 	(-0.06%)
229 	Bank of New York Mellon Corp 	BK 	0.088645 	  44.38 	-0.28 	(-0.62%)
230 	Verisk Analytics Inc 	VRSK 	0.088314 	  226.06 	1.54 	(0.69%)
231 	Vici Properties Inc 	VICI 	0.088073 	  31.96 	-0.38 	(-1.18%)
232 	Fidelity National Info Serv 	FIS 	0.088057 	  54.66 	-0.12 	(-0.22%)
233 	Devon Energy Corp 	DVN 	0.088032 	  48.29 	-1.51 	(-3.03%)
234 	Illumina Inc 	ILMN 	0.087723 	  201.84 	-4.03 	(-1.96%)
235 	Fastenal Co 	FAST 	0.087634 	  56.80 	0.22 	(0.38%)
236 	Consolidated Edison Inc 	ED 	0.087522 	  92.02 	-0.95 	(-1.02%)
237 	Resmed Inc 	RMD 	0.086955 	  216.99 	-2.05 	(-0.94%)
238 	Prudential Financial Inc 	PRU 	0.086756 	  85.08 	-1.95 	(-2.25%)
239 	Dupont De Nemours Inc 	DD 	0.086279 	  68.81 	-0.60 	(-0.86%)
240 	Public Service Enterprise Gp 	PEG 	0.084546 	  61.97 	-0.57 	(-0.91%)
241 	Digital Realty Trust Inc 	DLR 	0.083246 	  105.06 	-0.12 	(-0.11%)
242 	Baker Hughes Co 	BKR 	0.082928 	  29.81 	-0.77 	(-2.50%)
243 	Lennar Corp A 	LEN 	0.082601 	  121.50 	1.48 	(1.24%)
244 	Constellation Energy 	CEG 	0.082277 	  91.98 	-0.91 	(-0.98%)
245 	Zimmer Biomet Holdings Inc 	ZBH 	0.081918 	  143.71 	-0.39 	(-0.27%)
246 	Kroger Co 	KR 	0.081491 	  45.82 	-0.36 	(-0.77%)
247 	Republic Services Inc 	RSG 	0.080807 	  146.05 	0.32 	(0.22%)
248 	Amerisourcebergen Corp 	ABC 	0.080295 	  184.42 	1.41 	(0.77%)
249 	Halliburton Co 	HAL 	0.080144 	  31.53 	-1.05 	(-3.24%)
250 	Keysight Technologies In 	KEYS 	0.080089 	  162.77 	-2.09 	(-1.27%)
251 	Old Dominion Freight Line 	ODFL 	0.079872 	  320.95 	-4.51 	(-1.39%)
252 	Allstate Corp 	ALL 	0.079858 	  108.68 	-2.49 	(-2.24%)
253 	Mettler Toledo International 	MTD 	0.079756 	  1,283.90 	-38.10 	(-2.88%)
254 	Discover Financial Services 	DFS 	0.079557 	  115.70 	0.38 	(0.33%)
255 	Kraft Heinz Co 	KHC 	0.079532 	  36.63 	-0.37 	(-0.99%)
256 	Ansys Inc 	ANSS 	0.079033 	  331.80 	-2.57 	(-0.77%)
257 	Wec Energy Group Inc 	WEC 	0.078126 	  90.10 	-1.33 	(-1.46%)
258 	American Water Works Co Inc 	AWK 	0.078004 	  148.00 	-0.98 	(-0.66%)
259 	Ge Healthcare Technology 	GEHC 	0.077352 	  78.83 	0.18 	(0.23%)
260 	Dollar Tree Inc 	DLTR 	0.076836 	  136.52 	0.30 	(0.22%)
261 	Warner Bros Discovery Inc 	WBD 	0.076748 	  12.17 	-0.63 	(-4.91%)
262 	Equifax Inc 	EFX 	0.07621 	  227.78 	-1.99 	(-0.87%)
263 	Gartner Inc 	IT 	0.076141 	  353.62 	-2.92 	(-0.82%)
264 	P G & E Corp 	PCG 	0.075891 	  16.87 	-0.54 	(-3.07%)
265 	United Rentals Inc 	URI 	0.075657 	  407.66 	4.57 	(1.13%)
266 	Vulcan Materials Co 	VMC 	0.074644 	  208.96 	1.65 	(0.80%)
267 	Aptiv Plc 	APTV 	0.07446 	  100.46 	-0.98 	(-0.96%)
268 	Delta Air Lines Inc 	DAL 	0.07445 	  42.52 	-0.27 	(-0.64%)
269 	Corning Inc 	GLW 	0.074044 	  34.90 	-0.96 	(-2.66%)
270 	Oneok Inc 	OKE 	0.073798 	  59.32 	-1.63 	(-2.67%)
271 	Keurig Dr Pepper Inc 	KDP 	0.073778 	  31.95 	-0.23 	(-0.70%)
272 	Xylem Inc 	XYL 	0.073302 	  113.41 	-0.03 	(-0.02%)
273 	Avalonbay Communities Inc 	AVB 	0.072938 	  190.12 	-2.33 	(-1.21%)
274 	West Pharmaceutical Services 	WST 	0.072719 	  366.00 	3.96 	(1.09%)
275 	Hp Inc 	HPQ 	0.072698 	  30.21 	-0.80 	(-2.56%)
276 	Edison International 	EIX 	0.072601 	  68.70 	-1.48 	(-2.11%)
277 	Albemarle Corp 	ALB 	0.072406 	  232.61 	4.44 	(1.95%)
278 	Quanta Services Inc 	PWR 	0.072097 	  185.90 	-0.05 	(-0.03%)
279 	Global Payments Inc 	GPN 	0.07187 	  101.21 	0.53 	(0.53%)
280 	Martin Marietta Materials 	MLM 	0.071858 	  430.57 	4.03 	(0.95%)
281 	Arch Capital Group Ltd 	ACGL 	0.071301 	  70.77 	-0.39 	(-0.55%)
282 	Ingersoll Rand Inc 	IR 	0.070888 	  64.28 	-0.24 	(-0.38%)
283 	T Rowe Price Group Inc 	TROW 	0.069507 	  112.60 	-1.59 	(-1.39%)
284 	Fortive Corp 	FTV 	0.06881 	  71.61 	-0.21 	(-0.30%)
285 	Eversource Energy 	ES 	0.068116 	  70.64 	-1.44 	(-2.00%)
286 	Willis Towers Watson Plc 	WTW 	0.068073 	  232.54 	-2.46 	(-1.05%)
287 	Sba Communications Corp 	SBAC 	0.067537 	  224.64 	-5.93 	(-2.57%)
288 	Enphase Energy Inc 	ENPH 	0.06705 	  172.10 	-9.71 	(-5.34%)
289 	State Street Corp 	STT 	0.066987 	  73.15 	-0.62 	(-0.84%)
290 	Cbre Group Inc A 	CBRE 	0.066594 	  77.06 	-0.75 	(-0.97%)
291 	Ebay Inc 	EBAY 	0.066238 	  44.88 	-0.18 	(-0.40%)
292 	Tractor Supply Company 	TSCO 	0.0656 	  217.04 	-1.90 	(-0.87%)
293 	Cdw Corp/de 	CDW 	0.065451 	  177.47 	-0.69 	(-0.38%)
294 	Align Technology Inc 	ALGN 	0.064892 	  331.67 	1.38 	(0.42%)
295 	Diamondback Energy Inc 	FANG 	0.06419 	  127.00 	-1.74 	(-1.35%)
296 	Dte Energy Company 	DTE 	0.063897 	  113.13 	-0.99 	(-0.87%)
297 	Cardinal Health Inc 	CAH 	0.063775 	  91.32 	0.07 	(0.08%)
298 	Church & Dwight Co Inc 	CHD 	0.063626 	  94.48 	-1.68 	(-1.75%)
299 	Walgreens Boots Alliance Inc 	WBA 	0.063524 	  32.40 	-0.28 	(-0.84%)
300 	Lyondellbasell Indu Cl A 	LYB 	0.063362 	  89.65 	-2.59 	(-2.81%)
301 	Mccormick & Co Non Vtg Shrs 	MKC 	0.062898 	  93.08 	0.43 	(0.47%)
302 	Monolithic Power Systems Inc 	MPWR 	0.062864 	  511.07 	-6.54 	(-1.26%)
303 	Weyerhaeuser Co 	WY 	0.062139 	  31.27 	0.27 	(0.85%)
304 	Baxter International Inc 	BAX 	0.062114 	  45.03 	-0.34 	(-0.74%)
305 	Ulta Beauty Inc 	ULTA 	0.062108 	  447.18 	-0.73 	(-0.16%)
306 	Hartford Financial Svcs Grp 	HIG 	0.061929 	  70.72 	-1.16 	(-1.61%)
307 	Genuine Parts Co 	GPC 	0.061844 	  159.55 	-1.92 	(-1.19%)
308 	Equity Residential 	EQR 	0.061658 	  66.11 	-0.62 	(-0.92%)
309 	Hewlett Packard Enterprise 	HPE 	0.06138 	  16.99 	-0.59 	(-3.33%)
310 	Take Two Interactive Softwre 	TTWO 	0.059639 	  139.07 	0.43 	(0.31%)
311 	Ameren Corporation 	AEE 	0.058881 	  82.78 	-1.30 	(-1.54%)
312 	Entergy Corp 	ETR 	0.058596 	  99.46 	-2.55 	(-2.50%)
313 	Steris Plc 	STE 	0.05741 	  213.32 	-0.29 	(-0.13%)
314 	Firstenergy Corp 	FE 	0.057259 	  39.18 	0.11 	(0.27%)
315 	M & T Bank Corp 	MTB 	0.056575 	  122.46 	-0.70 	(-0.57%)
316 	Royal Caribbean Cruises Ltd 	RCL 	0.056343 	  96.60 	1.30 	(1.36%)
317 	Laboratory Crp of Amer Hldgs 	LH 	0.056237 	  232.04 	-2.23 	(-0.95%)
318 	Dover Corp 	DOV 	0.056148 	  143.56 	-4.17 	(-2.83%)
319 	Verisign Inc 	VRSN 	0.055582 	  221.63 	-2.06 	(-0.92%)
320 	Intl Flavors & Fragrances 	IFF 	0.055495 	  79.29 	-1.06 	(-1.32%)
321 	Darden Restaurants Inc 	DRI 	0.054927 	  166.02 	0.01 	(0.01%)
322 	Hologic Inc 	HOLX 	0.054915 	  82.10 	0.90 	(1.11%)
323 	Southwest Airlines Co 	LUV 	0.054805 	  34.47 	0.22 	(0.63%)
324 	Fair Isaac Corp 	FICO 	0.054599 	  795.65 	-4.31 	(-0.54%)
325 	Invitation Homes Inc 	INVH 	0.053833 	  34.36 	-0.05 	(-0.13%)
326 	Insulet Corp 	PODD 	0.05371 	  288.71 	4.21 	(1.48%)
327 	Ppl Corp 	PPL 	0.053583 	  26.71 	-0.28 	(-1.02%)
328 	Extra Space Storage Inc 	EXR 	0.052794 	  144.05 	-1.23 	(-0.85%)
329 	Omnicom Group 	OMC 	0.05257 	  93.84 	-1.31 	(-1.38%)
330 	Clorox Company 	CLX 	0.05247 	  155.60 	-0.94 	(-0.60%)
331 	Raymond James Financial Inc 	RJF 	0.052351 	  99.00 	-1.09 	(-1.09%)
332 	Coterra Energy Inc 	CTRA 	0.051874 	  24.46 	-0.75 	(-2.98%)
333 	Las Vegas Sands Corp 	LVS 	0.05184 	  58.76 	0.31 	(0.54%)
334 	Teledyne Technologies Inc 	TDY 	0.051686 	  399.64 	-6.79 	(-1.67%)
335 	Broadridge Financial Solutio 	BR 	0.051254 	  158.71 	-2.09 	(-1.30%)
336 	Wabtec Corp 	WAB 	0.050891 	  101.98 	-1.66 	(-1.60%)
337 	First Solar Inc 	FSLR 	0.050759 	  185.76 	-3.23 	(-1.71%)
338 	Ventas Inc 	VTR 	0.05001 	  45.52 	-0.56 	(-1.22%)
339 	Centerpoint Energy Inc 	CNP 	0.049843 	  29.10 	-0.08 	(-0.26%)
340 	Ball Corp 	BALL 	0.049572 	  56.11 	-2.32 	(-3.98%)
341 	Fifth Third Bancorp 	FITB 	0.049349 	  26.74 	0.20 	(0.75%)
342 	Alexandria Real Estate Equit 	ARE 	0.049341 	  114.05 	-1.40 	(-1.22%)
343 	Expeditors Intl Wash Inc 	EXPD 	0.049323 	  115.83 	-3.00 	(-2.52%)
344 	Cooper Cos Inc 	COO 	0.049188 	  369.11 	1.70 	(0.46%)
345 	Nvr Inc 	NVR 	0.04897 	  5,982.21 	-8.17 	(-0.14%)
346 	Fleetcor Technologies Inc 	FLT 	0.048679 	  243.16 	-0.47 	(-0.19%)
347 	Mid America Apartment Comm 	MAA 	0.048659 	  153.57 	-1.72 	(-1.11%)
348 	Cms Energy Corp 	CMS 	0.047998 	  60.14 	-0.60 	(-0.99%)
349 	United Airlines Holdings Inc 	UAL 	0.047373 	  52.72 	-0.78 	(-1.46%)
350 	Skyworks Solutions Inc 	SWKS 	0.047276 	  107.40 	-1.86 	(-1.70%)
351 	Teradyne Inc 	TER 	0.047018 	  108.81 	-2.25 	(-2.03%)
352 	Nasdaq Inc 	NDAQ 	0.046874 	  51.65 	0.43 	(0.84%)
353 	Steel Dynamics Inc 	STLD 	0.046107 	  100.93 	-1.60 	(-1.56%)
354 	Principal Financial Group 	PFG 	0.046096 	  73.07 	-1.71 	(-2.28%)
355 	Regions Financial Corp 	RF 	0.046047 	  17.90 	-0.23 	(-1.24%)
356 	Kellogg Co 	K 	0.045965 	  65.62 	-0.68 	(-1.02%)
357 	Howmet Aerospace Inc 	HWM 	0.045843 	  46.59 	0.61 	(1.32%)
358 	Atmos Energy Corp 	ATO 	0.045445 	  116.08 	-0.92 	(-0.78%)
359 	Pultegroup Inc 	PHM 	0.044987 	  74.88 	1.37 	(1.86%)
360 	Iron Mountain Inc 	IRM 	0.044771 	  55.41 	-1.35 	(-2.39%)
361 	Conagra Brands Inc 	CAG 	0.044491 	  34.26 	-0.39 	(-1.11%)
362 	Tyler Technologies Inc 	TYL 	0.04442 	  391.82 	-1.98 	(-0.50%)
363 	Jm Smucker Co 	SJM 	0.04436 	  151.59 	-1.51 	(-0.99%)
364 	Lamb Weston Holdings Inc 	LW 	0.044331 	  113.48 	-0.86 	(-0.75%)
365 	Garmin Ltd 	GRMN 	0.044146 	  105.42 	-0.58 	(-0.55%)
366 	Netapp Inc 	NTAP 	0.043779 	  72.87 	-1.50 	(-2.02%)
367 	Targa Resources Corp 	TRGP 	0.043777 	  70.93 	-0.86 	(-1.20%)
368 	Factset Research Systems Inc 	FDS 	0.043696 	  421.95 	1.04 	(0.25%)
369 	Molina Healthcare Inc 	MOH 	0.043648 	  279.50 	1.48 	(0.53%)
370 	Waters Corp 	WAT 	0.043494 	  262.93 	-6.27 	(-2.33%)
371 	Cincinnati Financial Corp 	CINF 	0.043348 	  98.98 	-1.92 	(-1.90%)
372 	Carnival Corp 	CCL 	0.042962 	  15.91 	0.11 	(0.66%)
373 	Idex Corp 	IEX 	0.042626 	  205.44 	-4.31 	(-2.06%)
374 	Best Buy Co Inc 	BBY 	0.042624 	  78.76 	-1.03 	(-1.29%)
375 	Huntington Bancshares Inc 	HBAN 	0.042306 	  10.74 	-0.19 	(-1.69%)
376 	Brown & Brown Inc 	BRO 	0.042253 	  66.09 	-0.17 	(-0.25%)
377 	Northern Trust Corp 	NTRS 	0.042249 	  73.43 	-1.28 	(-1.72%)
378 	Interpublic Group of Cos Inc 	IPG 	0.042148 	  39.53 	-0.52 	(-1.29%)
379 	Paycom Software Inc 	PAYC 	0.042126 	  322.46 	2.54 	(0.79%)
380 	Amcor Plc 	AMCR 	0.042024 	  10.21 	-0.15 	(-1.40%)
381 	Solaredge Technologies Inc 	SEDG 	0.041957 	  255.45 	-21.20 	(-7.68%)
382 	Quest Diagnostics Inc 	DGX 	0.041735 	  138.26 	-0.34 	(-0.24%)
383 	Ptc Inc 	PTC 	0.041334 	  141.74 	-1.41 	(-0.99%)
384 	Essex Property Trust Inc 	ESS 	0.041146 	  234.42 	-2.50 	(-1.05%)
385 	Everest Re Group Ltd 	RE 	0.041042 	  352.79 	0.44 	(0.12%)
386 	Expedia Group Inc 	EXPE 	0.041013 	  106.86 	0.99 	(0.94%)
387 	Revvity Inc 	RVTY 	0.040872 	  115.97 	-3.30 	(-2.76%)
388 	Jacobs Solutions Inc 	J 	0.04058 	  115.53 	-1.04 	(-0.89%)
389 	Marathon Oil Corp 	MRO 	0.040428 	  22.87 	-0.64 	(-2.70%)
390 	Hunt (Jb) Transprt Svcs Inc 	JBHT 	0.039724 	  174.03 	-2.65 	(-1.50%)
391 	Snap on Inc 	SNA 	0.03952 	  273.55 	-0.32 	(-0.12%)
392 	Zebra Technologies Corp Cl A 	ZBRA 	0.039471 	  277.69 	-4.71 	(-1.67%)
393 	Bunge Ltd 	BG 	0.039282 	  93.41 	-3.03 	(-3.14%)
394 	Akamai Technologies Inc 	AKAM 	0.039219 	  90.71 	-0.79 	(-0.86%)
395 	Cboe Global Markets Inc 	CBOE 	0.039173 	  136.87 	-0.49 	(-0.36%)
396 	Eqt Corp 	EQT 	0.039063 	  39.29 	-0.35 	(-0.89%)
397 	Tyson Foods Inc Cl A 	TSN 	0.039043 	  49.91 	-0.48 	(-0.96%)
398 	Synchrony Financial 	SYF 	0.039013 	  32.77 	-0.14 	(-0.41%)
399 	Aes Corp 	AES 	0.038676 	  20.97 	-0.38 	(-1.76%)
400 	Axon Enterprise Inc 	AXON 	0.038585 	  205.03 	2.67 	(1.32%)
401 	Textron Inc 	TXT 	0.038053 	  66.04 	-0.60 	(-0.90%)
402 	Avery Dennison Corp 	AVY 	0.03792 	  168.50 	-2.59 	(-1.52%)
403 	Cf Industries Holdings Inc 	CF 	0.037879 	  71.75 	0.48 	(0.67%)
404 	Pool Corp 	POOL 	0.037849 	  353.49 	-4.46 	(-1.25%)
405 	Stanley Black & Decker Inc 	SWK 	0.037817 	  89.39 	-1.51 	(-1.66%)
406 	Lkq Corp 	LKQ 	0.037284 	  54.23 	-0.01 	(-0.01%)
407 	Evergy Inc 	EVRG 	0.03694 	  58.85 	-0.47 	(-0.78%)
408 	Alliant Energy Corp 	LNT 	0.036608 	  52.95 	-0.79 	(-1.47%)
409 	Fmc Corp 	FMC 	0.03631 	  105.40 	-1.37 	(-1.28%)
410 	Citizens Financial Group 	CFG 	0.036201 	  27.21 	-0.05 	(-0.19%)
411 	Udr Inc 	UDR 	0.036002 	  42.93 	-0.50 	(-1.14%)
412 	Trimble Inc 	TRMB 	0.035425 	  51.60 	-1.07 	(-2.04%)
413 	Western Digital Corp 	WDC 	0.035063 	  39.07 	-1.40 	(-3.45%)
414 	Mgm Resorts International 	MGM 	0.034977 	  43.12 	0.48 	(1.11%)
415 	Carmax Inc 	KMX 	0.034684 	  78.69 	-0.94 	(-1.18%)
416 	Live Nation Entertainment In 	LYV 	0.034581 	  89.01 	-1.17 	(-1.30%)
417 	Nordson Corp 	NDSN 	0.034532 	  235.47 	-1.64 	(-0.69%)
418 	Epam Systems Inc 	EPAM 	0.033994 	  219.34 	-0.17 	(-0.08%)
419 	Viatris Inc 	VTRS 	0.033858 	  10.20 	-0.10 	(-0.92%)
420 	Camden Property Trust 	CPT 	0.033807 	  111.68 	-1.43 	(-1.26%)
421 	Masco Corp 	MAS 	0.033792 	  56.16 	0.66 	(1.20%)
422 	Packaging Corp of America 	PKG 	0.033655 	  131.86 	-0.57 	(-0.43%)
423 	Molson Coors Beverage Co B 	TAP 	0.033606 	  66.63 	0.35 	(0.52%)
424 	Seagate Technology Holdings 	STX 	0.033497 	  62.63 	-1.67 	(-2.60%)
425 	Bio Techne Corp 	TECH 	0.033497 	  77.51 	-0.98 	(-1.25%)
426 	Host Hotels & Resorts Inc 	HST 	0.033079 	  16.60 	-0.46 	(-2.67%)
427 	Mosaic Co 	MOS 	0.033036 	  34.84 	-0.98 	(-2.73%)
428 	Wr Berkley Corp 	WRB 	0.032646 	  58.47 	-0.82 	(-1.37%)
429 	Jack Henry & Associates Inc 	JKHY 	0.032277 	  163.49 	-0.05 	(-0.03%)
430 	Hormel Foods Corp 	HRL 	0.032245 	  40.82 	-0.46 	(-1.10%)
431 	Kimco Realty Corp 	KIM 	0.032194 	  19.23 	-0.22 	(-1.14%)
432 	Etsy Inc 	ETSY 	0.03213 	  96.18 	1.58 	(1.67%)
433 	Teleflex Inc 	TFX 	0.032125 	  253.30 	0.90 	(0.36%)
434 	Domino S Pizza Inc 	DPZ 	0.032087 	  325.33 	-6.08 	(-1.83%)
435 	Match Group Inc 	MTCH 	0.032047 	  42.42 	0.17 	(0.39%)
436 	Brown Forman Corp Class B 	BF.B 	0.031947 	  64.91 	-0.49 	(-0.75%)
437 	Incyte Corp 	INCY 	0.031807 	  61.74 	-1.49 	(-2.36%)
438 	Leidos Holdings Inc 	LDOS 	0.031627 	  85.33 	-0.56 	(-0.65%)
439 	Borgwarner Inc 	BWA 	0.031282 	  46.43 	-2.17 	(-4.46%)
440 	International Paper Co 	IP 	0.031223 	  31.59 	-0.39 	(-1.23%)
441 	Loews Corp 	L 	0.030841 	  58.08 	-0.49 	(-0.83%)
442 	Celanese Corp 	CE 	0.030676 	  109.07 	-4.93 	(-4.33%)
443 	Healthpeak Properties Inc 	PEAK 	0.030666 	  20.21 	-0.47 	(-2.25%)
444 	Apa Corp 	APA 	0.030311 	  33.54 	-0.84 	(-2.45%)
445 	C.H. Robinson Worldwide Inc 	CHRW 	0.030169 	  92.68 	-1.94 	(-2.05%)
446 	Nisource Inc 	NI 	0.029893 	  27.22 	-0.16 	(-0.57%)
447 	Wynn Resorts Ltd 	WYNN 	0.029387 	  106.21 	2.48 	(2.39%)
448 	American Airlines Group Inc 	AAL 	0.029095 	  16.35 	-0.14 	(-0.82%)
449 	Charles River Laboratories 	CRL 	0.028982 	  209.85 	-0.14 	(-0.07%)
450 	Gen Digital Inc 	GEN 	0.028967 	  18.57 	-0.06 	(-0.34%)
451 	Henry Schein Inc 	HSIC 	0.028653 	  77.95 	-0.08 	(-0.10%)
452 	Allegion Plc 	ALLE 	0.028405 	  118.21 	-0.22 	(-0.18%)
453 	Tapestry Inc 	TPR 	0.028299 	  43.54 	0.17 	(0.38%)
454 	Juniper Networks Inc 	JNPR 	0.028227 	  31.50 	-0.98 	(-3.00%)
455 	Marketaxess Holdings Inc 	MKTX 	0.02815 	  274.65 	-2.50 	(-0.90%)
456 	Caesars Entertainment Inc 	CZR 	0.028024 	  49.21 	0.37 	(0.76%)
457 	Qorvo Inc 	QRVO 	0.027803 	  102.83 	0.21 	(0.20%)
458 	Ceridian Hcm Holding Inc 	CDAY 	0.027726 	  67.45 	0.37 	(0.55%)
459 	Pentair Plc 	PNR 	0.026956 	  60.89 	0.08 	(0.13%)
460 	Eastman Chemical Co 	EMN 	0.026863 	  80.41 	-2.26 	(-2.74%)
461 	Globe Life Inc 	GL 	0.02639 	  106.81 	-1.20 	(-1.11%)
462 	Universal Health Services B 	UHS 	0.025823 	  149.35 	0.73 	(0.49%)
463 	Rollins Inc 	ROL 	0.025764 	  40.98 	-0.12 	(-0.28%)
464 	Regency Centers Corp 	REG 	0.02555 	  60.70 	-0.44 	(-0.72%)
465 	Campbell Soup Co 	CPB 	0.025364 	  45.85 	-0.58 	(-1.24%)
466 	Pinnacle West Capital 	PNW 	0.025263 	  82.59 	-0.66 	(-0.79%)
467 	Keycorp 	KEY 	0.025147 	  9.87 	-0.07 	(-0.65%)
468 	Smith (a.O.) Corp 	AOS 	0.024598 	  70.10 	-0.91 	(-1.27%)
469 	Fox Corp Class A 	FOXA 	0.024589 	  33.28 	-0.37 	(-1.09%)
470 	F5 Inc 	FFIV 	0.024402 	  149.09 	-2.89 	(-1.90%)
471 	Bath & Body Works Inc 	BBWI 	0.023977 	  38.82 	-0.13 	(-0.33%)
472 	Huntington Ingalls Industrie 	HII 	0.023743 	  218.16 	-3.02 	(-1.37%)
473 	Dentsply Sirona Inc 	XRAY 	0.023215 	  39.26 	-0.48 	(-1.20%)
474 	Paramount Global Class B 	PARA 	0.022189 	  15.67 	-0.61 	(-3.76%)
475 	Robert Half Intl Inc 	RHI 	0.021816 	  71.73 	-1.69 	(-2.30%)
476 	Nrg Energy Inc 	NRG 	0.02167 	  33.52 	-0.60 	(-1.75%)
477 	Bio Rad Laboratories A 	BIO 	0.021653 	  371.24 	-5.32 	(-1.41%)
478 	Catalent Inc 	CTLT 	0.021553 	  44.22 	0.11 	(0.26%)
479 	Whirlpool Corp 	WHR 	0.021537 	  146.65 	0.14 	(0.10%)
480 	Norwegian Cruise Line Holdin 	NCLH 	0.02141 	  19.32 	0.19 	(0.97%)
481 	Hasbro Inc 	HAS 	0.021148 	  61.58 	0.13 	(0.21%)
482 	Boston Properties Inc 	BXP 	0.020904 	  54.19 	-0.85 	(-1.54%)
483 	Franklin Resources Inc 	BEN 	0.020871 	  26.43 	-0.54 	(-2.00%)
484 	News Corp Class A 	NWSA 	0.020607 	  19.10 	-0.48 	(-2.43%)
485 	Invesco Ltd 	IVZ 	0.020602 	  16.54 	-0.25 	(-1.46%)
486 	Westrock Co 	WRK 	0.020221 	  28.66 	-0.83 	(-2.80%)
487 	Generac Holdings Inc 	GNRC 	0.02016 	  129.28 	9.86 	(8.25%)
488 	Federal Realty Invs Trust 	FRT 	0.019006 	  94.32 	-1.61 	(-1.68%)
489 	Assurant Inc 	AIZ 	0.018898 	  129.38 	-2.06 	(-1.57%)
490 	Vf Corp 	VFC 	0.017488 	  19.75 	0.24 	(1.20%)
491 	Dxc Technology Co 	DXC 	0.017021 	  27.37 	-0.08 	(-0.27%)
492 	Alaska Air Group Inc 	ALK 	0.016873 	  49.59 	-0.83 	(-1.65%)
493 	Sealed Air Corp 	SEE 	0.016207 	  39.93 	-0.51 	(-1.25%)
494 	Comerica Inc 	CMA 	0.015073 	  42.27 	-0.15 	(-0.35%)
495 	Davita Inc 	DVA 	0.014678 	  97.90 	0.28 	(0.29%)
496 	Organon & Co 	OGN 	0.014252 	  20.92 	0.01 	(0.02%)
497 	Mohawk Industries Inc 	MHK 	0.013986 	  101.05 	0.15 	(0.15%)
498 	Ralph Lauren Corp 	RL 	0.013701 	  123.55 	0.37 	(0.30%)
499 	Fox Corp Class B 	FOX 	0.011886 	  31.07 	-0.44 	(-1.38%)
500 	Zions Bancorp Na 	ZION 	0.011651 	  27.87 	-0.77 	(-2.67%)
501 	Advance Auto Parts Inc 	AAP 	0.011313 	  68.16 	-1.06 	(-1.53%)
502 	Lincoln National Corp 	LNC 	0.010192 	  24.33 	-0.04 	(-0.17%)
503 	Newell Brands Inc 	NWL 	0.008666 	  8.29 	-0.23 	(-2.64%)
504 	News Corp Class B 	NWS 	0.00654 	  19.35 	-0.46 	(-2.30%)'''


if __name__ == "__main__":
    rows = RAW.split('\n')

    final = {}
    for row in rows[1:]:
        components = row.split('\t')
        print(components)
        final[components[2]] = components[3]

    for key, value in final.items():
        print(key)
        print(value)
    target = Path(__file__).parent.parent / 'py_portfolio_index' / 'bin' /  'indexes' / 'sp500_2023_q3.csv'

    with open(target, 'w') as f:
        for key, value in final.items():
            f.write(f'{key.strip()},{value.strip()}\n')
    

## 	Company 	Symbol 	Weight 	      Price 	Chg 	% Chg