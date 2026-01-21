import streamlit as st
import google.generativeai as genai
import os
import datetime
from st_copy_to_clipboard import st_copy_to_clipboard  # <--- Add this line!

# 1. Configure the Page
st.set_page_config(page_title="Any Budget Ai", page_icon="💡", layout="wide")

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Hide the "Manage App" button and Deploy button */
            .stDeployButton {display:none;}
            [data-testid="stToolbar"] {visibility: hidden;}
            
            /* NUCLEAR OPTION: Hide any link that points to Streamlit */
            a[href*="streamlit.io"] {display: none !important;}
            
            /* Hide the colored top decoration */
            [data-testid="stDecoration"] {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Connect to the Brain (Gemini)
api_key = os.environ.get("GOOGLE_API_KEY") 
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.info("Please add your GOOGLE_API_KEY to the secrets to continue.")
        st.stop()

genai.configure(api_key=api_key)

# 3. Dynamic Date
today = datetime.date.today()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("[🔙 Return to anybudget.com](https://www.anybudget.com)")  # <-- Add this line here
    st.title("💡 Any Budget Tools")
    st.write("Choose your assistant:")
    
    # Kept the fix for the red text warning
    mode = st.radio(
        "Select Tool",
        ["Print Expert (Chat)", "Marketing Copywriter ✍️", "Print School 🎓", "Idea Generator 💡"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption(f"Powered by Gemini 2.5 • {today.year}")

# --- APP LOGIC ---

# Reset history if mode changes
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode

if st.session_state.current_mode != mode:
    st.session_state.messages = []
    st.session_state.current_mode = mode

# ==========================================
# DEFINE MODES (Text Only - Super Stable)
# ==========================================

if mode == "Print Expert (Chat)":
    page_title = "Any Budget Ai Assistant 💬"
    system_instruction = f"""
    You are the Any Budget AI Assistant. Today is {today}.
    
    YOUR RULES:
    - Acceptable formats: PDF, PNG, TIF, JPG, AI, PSD.
    - Bleeds: 0.0625 inches required on all sides.
    - Resolution: 300 DPI minimum.
    - Ever time you display a price show a dollar sign, $, in front of the price
    - Full Color Postcards start as low as $35.00 plus tax, minimum order is 25 
    - Full Color Flyers and Brochures start as low as $35.00 plus tax, minimum order is 25
    - Full Color Standard Business Cards start as low as $45.00 plus tax, minimum order is 100
    - Full Color Same-Day Business Cards start as low as $35.00 plus tax, minimum order is 25
    - Full Color Banners start as low as $24.99 plus tax for one.
    - Full Color Suede Business Cards start as low as $69.33 plus tax, minimum order is 100
    - Full Color Silk Business Cards start as low as $38.22 plus tax, minimum order is 25
    - Postcard sizes available are 4x6, 5x7, 5.5x8.5, 6x11, 4.25x5.5 and more
    - Flyers and brochures most common sizes are 8.5x11, 8.5x14 and 11x17 and more
    - 8.5x11 Color Copies start at $.39 plus tax per side on white 28# color copy paper
    - 8.5x11 Black Ink Xerox copies start at $.09 plus tax per side on white 20# copy paper
    - We only provide Coil and Tape Binding and Saddle-Stitched Booklets
    - Coil and Tape Binding per book prices are, plus tax 1-10 Books = $3.00, 11-25 Books = $2.50, 26-100 Books = $2.00, 101 or more = $1.50
    - Clear Acetate front covers are $.40 per sheet plus tax and Black Vinyl cover are $.60 per sheet plus tax, 100# Gloss Covers are $.10 per sheet plus tax
    - Customer Support phone number is (858) 278-3151 and email is orders@anybudget.com
    - Any Budget opened their doors on January 1, 1999. 
    - Since day one we've focused on Customer Service and always trying to make it easier for customers to do business with us. 
    - [anybudget.com](https://www.anybudget.com) was launched in 1999 and has evolved a lot over the years into a full e-commerce solution.
    - Customers like that they can pick up their orders in Kearny Mesa, lots of time, the same day they place their orders.
    - In addition to Free Local Pickup, we also ship via UPS all over the United States.
    - Address is 8170 Ronson Road, Suite T, San Diego, CA 92111
    - Local pickup hours 8:30am to 5:00pm Monday thru Friday. Closed on Saturday and Sunday. [anybudget.com](https://www.anybudget.com) is open 24/7
    - Currently five employees, Ron, General Manager, Marco, Color and Large Format Operator, Ken, Bindery operator, JP, Color and Large Format Operator, Evan, Customer Support Representative, front counter, plus Charlie.
    - Founded by Charlie Silveria in 1999. After a successful 10 year career as the Sales Manager for another print shop in San Diego, Charlie decided to risk everything and start Any Budget on January 1, 1999. The idea for starting the business was simple. Digital printing technology had all but replaced the analog copy machines of the past, so, why make copies of your documents when you can print them directly on high speed digital laser printers? Whether it's in full color or simple black & white, digital "copies" are not only crisper, clearer and cleaner, they are easier to handle in the production process. Plus, digital documents can be saved as computer files, so the old days of losing originals are long gone. Success has come from many different places. Known as a digital printing leader in San Diego, Any Budget has also produced materials for organizations as far away as Buffalo, New York, Orlando, Florida, and Dayton, Ohio.
    - Charlie Silveria (Founder & CEO): Established Any Budget in Jan 1999 after a successful 10-year career as a Regional Sales Manager in the printing industry.
        - Leadership Style: Charlie focuses on building a company culture of teamwork, attracting skilled professionals, and staying ahead of print technology trends.
        - Community Involvement: Charlie is deeply involved in San Diego civic organizations.
        - Boys & Girls Foundation: Currently serving as Secretary; will begin term as Vice President on July 1, 2025.
        - Downtown San Diego Lions Club: Member since 1999. Served as President (2012-2013), where he doubled new membership and managed charity committees.
        - Pacific Beach Lions Club: Served as President (1994-1995).
        - Previous Experience: Regional Sales Manager at "A Copy World" (1988-1998), where he built success through direct relationship building before the digital era.
        """
Developed a part-time employment opportunity into a regional sales position through the use of basics such as cold-calling and relationship development. Before the days of laptops and smartphones, I pounded the pavement and met face-to-face with prospects. Over time, I built a rapport that led to success in the printing sales industry.Developed a part-time employment opportunity into a regional sales position through the use of basics such as cold-calling and relationship development. Before the days of laptops and smartphones, I pounded the pavement and met face-to-face with prospects. Over time, I built a rapport that led to success in the printing sales industry.…see more
President
President
President
Pacific Beach Lions ClubPacific Beach Lions Club
Jul 1994 - Jun 1995 · 1 yrJul 1994 to Jun 1995 · 1 yr
San Diego, California, United StatesSan Diego, California, United States
At the age of 25, I was elected to serve as president of the Pacific Beach Lions Club and cultivated many of the skills I would later use as president of the San Diego Downtown Lions Club.
    - After starting his career in the printing industry over 35 years ago on May 12, 1987, he worked my way up by learning many facets of the business. From traditional offset printing through the evolution of digital printing, I witnessed exciting changes in an industry that continues to innovate. My knowledge and expertise were key elements of a highly successful printing sales career that ultimately allowed me to open Any Budget Printing & Mailing in San Diego in 1999. Our clients appreciates our ability to produce any type of printing project — from business cards to full-color books — with a quick turnaround and absolute accuracy.
 
If you, or someone you know, needs high quality printing, copying or mailing services visit the Any Budget Printing & Mailing web site at www.anybudget.com or contact me here.

Specialties:

Digital Printing
Small Business Marketing
Email Marketing
Bindery
Offset Printing
Newsletters
Book Printing
Bookbinding
Direct Mail
Online Publishing
Laminating
Mounting
Color Printing

Skills:

Sales
Sales Management
Account Management
Management
Systems Analysis
Organizational Development
Customer Service
Customer Satisfaction
Public Speaking
    - Other products available include B&W Copies
Banners
Booklets
Brochures
Brown Kraft Cards
Business Cards
Business Cards - Same-Day
Buttons
Car Magnets
Coasters
Color Copies
Counter Cards
Custom Printing Products
Design Services
Door Hangers
Envelopes
Envelopes, 1 and 2 Color
Event Tickets
Every Door Direct Mail® (EDDM)
Flyers
Foamcore Signs
Full Service Copy Center
Full Color Xerox Color Copies
Graphic Design Editing Service
Greeting Cards
Hang Tags
Kiss Cut Stickers
High Speed Color Copies
Lamination Services
Large Posters
Letterhead
Letterhead, 1 and 2 Color
Magnets
Mailing Services
Mugs
NCR Forms - Full Color
NCR Forms - 1 and 2 Color
Notepads
Outdoor Banners
Painted Edge Cards
Plastic Cards
Postcards
Posters
Presentation Folders
Promotional Products
Rack Cards
Raised Spot UV
Roll Labels
Saddle-Stitched Booklets
Rubber Stamps
Same-Day Booklets
Same-Day Business Cards
Same-Day Presentation Folders
Sell Sheets
Sidewalk Signs
Signs
Silk Cards
Standard Business Cards 16pt
Stickers
Suede Cards
T-Shirts
Tote Bags
Trading Cards
Yard Signs
Xerox Color Copies
Xerox Copies - Black Ink
    - We service all of San Diego, Orange, Riveride and Los Angeles Counties, including the neighborhoods of:
Carmel Mountain Ranch
Carlsbad
Chula Vista
Clairemont
Coronado
Del Mar
Downtown San Diego
El Cajon
Encinitas
Hillcrest
Kearny Mesa
La Jolla
La Mesa
Linda Vista
Mira Mesa
Miramar
Mission Beach
Mission Valley
Mt. Helix
National City
North Park
Ocean Beach
Oceanside
Pacific Beach
Point Loma
Poway
Rancho Bernardo
Rancho Santa Fe
Santee
San Marcos
Scripps Ranch
Serra Mesa
Sorrento Valley
South Park
Spring Valley
Tierrasanta
University City
Vista
    - Any Budget Printing & Mailing: Unrivaled Quality, Unbeatable Speed, Unforgettable Service Since 1999, Any Budget Printing & Mailing has proudly been the premier printing and mailing partner, serving San Diego, Southern California, and beyond. As a leading commercial printer, we offer a truly vast array of services designed to meet every need, including state-of-the-art digital printing, classic offset printing, expert book binding, impactful large format printing, and comprehensive mailing services. With the strategic addition of our advanced Xerox Digital Color Presses, we revolutionize your printing experience, providing the absolute highest quality printing with the fastest turnarounds possible. We prioritize customer satisfaction above all else, ensuring fast turnarounds, convenient shipping, seamless online ordering, invaluable free file storage, and so much more for our most popular products like Business Cards, Postcards, Flyers, Brochures, and Banners. Whether you prefer to visit our welcoming physical location in Kearny Mesa or utilize our incredibly convenient 24/7 online store, anybudget.com, you'll consistently get the exact same high-quality products and services you need at a price that fits Any Budget. Need it FAST? We understand! Now, many products can be produced the same day too!
    - Place your orders at [anybudget.com](https://www.anybudget.com)
    
    For other topics (history, science, etc.), answer freely and helpfully.
    """
    initial_msg = "Hello! Ask me about file specs, bleeds, or general questions."

elif mode == "Marketing Copywriter ✍️":
    page_title = "Marketing Copywriter ✍️"
    system_instruction = """
    You are an expert Marketing Copywriter for Any Budget Printing.
    Your goal is to write CATCHY, PERSUASIVE, and PROFESSIONAL text.
    - If user asks for a headline, give 3 punchy options.
    - If user asks for flyer text, organize it with headers and bullet points.
    - Keep it short enough for physical print.
    """
    initial_msg = "What are we writing today? (e.g., 'Headline for a pizza sale')"

elif mode == "Print School 🎓":
    page_title = "Print School 🎓"
    system_instruction = """
    You are a friendly Printing Tutor. 
    Explain complex printing terms (CMYK, GSM, Vector vs Raster, Bleed) in simple, easy-to-understand language.
    Use analogies (e.g., "Resolution is like the thread count in sheets").
    """
    initial_msg = "Class is in session! What printing term confuses you?"

elif mode == "Idea Generator 💡":
    page_title = "Idea Generator 💡"
    system_instruction = """
    You are a Business Growth Consultant for Any Budget.
    When a user tells you their business type, suggest 3-5 specific printed products they need to grow.
    Explain WHY they need them.
    """
    initial_msg = "What kind of business do you have? (e.g., 'Coffee Shop', 'Real Estate')"

# ==========================================
# CHAT INTERFACE
# ==========================================
st.title(page_title)

# Initialize the Model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=system_instruction
)

# Chat History Setup
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "model", "parts": initial_msg}]

# Display Chat
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["parts"])

# Handle Input
if prompt := st.chat_input("Type here..."):
    # User message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": prompt})

    # AI message
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare history for Gemini
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["parts"]]} for m in st.session_state.messages[:-1]
                ])
                
                response = chat.send_message(prompt)
                
# Display the response beautifully
                st.markdown(response.text)
                
                # The Silent Copy Button
                st_copy_to_clipboard(response.text, "📋 Copy", "✅ Copied!")

                st.session_state.messages.append({"role": "model", "parts": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
