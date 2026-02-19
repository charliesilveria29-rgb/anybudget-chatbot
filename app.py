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

# ==========================================
# PRICING DATA
# ==========================================
POSTCARD_PRICES = """
HERE IS THE OFFICIAL POSTCARD PRICING SHEET (2026).
USE THIS TABLE TO QUOTE PRICES. IF A QUANTITY OR SIZE IS N/A, SAY WE CANNOT PRINT IT.

| Size | Sides | 25 | 50 | 75 | 100 | 250 | 500 | 1000 | 2500 | 5000 | 7500 | 10000 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 4" X 6" | 4/0 or 4/4 | $35 | $45 | $55 | $65 | $75 | $85 | $125 | $245 | $295 | $345 | $495 |
| 2" X 6" | 4/0 | $35 | $45 | $55 | $65 | $75 | $85 | $125 | $145 | $175 | N/A | $200.72 |
| 3.5" X 5" | 4/0 or 4/4 | N/A | N/A | N/A | N/A | N/A | N/A | $81.02 | $131.95 | $204.05 | N/A | $388.44 |
| 4.25" X 11" | 4/0 or 4/4 | $55 | $65 | $75 | $95 | $145 | $175 | $195 | $295 | $495 | N/A | $975 |
| 4.25" X 5.5" | 4/0 or 4/4 | $35 | $45 | $55 | $65 | $75 | $85 | $125 | $245 | $295 | N/A | $495 |
| 4.25" X 6" | 4/0 or 4/4 | N/A | N/A | N/A | $65 | $75 | $85 | $125 | $245 | $295 | N/A | $495 |
| 5" X 7" | 4/0 or 4/4 | $55 | $65 | $75 | $85 | $145 | $175 | $195 | $245 | $395 | $595 | $795 |
| 6" X 11" | 4/0 or 4/4 | $45 | $65 | $85 | $105 | $175 | $195 | $295 | $495 | $695 | $1,095 | $1,395 |
| 6" X 9" | 4/0 or 4/4 | $45 | $65 | $85 | $105 | $175 | $195 | $295 | $395 | $595 | $895 | $1,095 |
| 3.667" X 8.5"| 4/0 | $55 | $65 | $75 | $85 | $125 | $145 | $178.75| $287.32| $441.67| N/A | $876.26 |
| 5.5" X 8.5" | 4/0 or 4/4 | $55 | $65 | $75 | $85 | $145 | $195 | $245 | $345 | $495 | $795 | $995 |
| 5" X 8" | 4/0 or 4/4 | N/A | N/A | N/A | $85 | $145 | $195 | $245 | $345 | $495 | N/A | $595 |
| 6" X 8.5" | 4/0 or 4/4 | $55 | $65 | $75 | $85 | $145 | $195 | $295 | $395 | $495 | N/A | $975 |
| 6" X 8" | 4/0 or 4/4 | N/A | N/A | N/A | $105 | $175 | $195 | $245 | $345 | $513.72 | $810.34 | $1019.44 |

Definition of Sides:
- 4/0 means Full Color Front, Blank Back.
- 4/4 means Full Color Front, Full Color Back.
"""


# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("[🔙 Return to anybudget.com](https://www.anybudget.com)")  # <-- Add this line here
    st.title("💡 Any Budget Ai Tools")
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

    base_instruction =
You are the AI Assistant for Any Budget Printing.
Your tone is helpful, professional, and concise.

IMPORTANT PRICING RULE:
- When you quote a price from the table, YOU MUST always add "plus tax" after the dollar amount.
- Example: "The price is $85 plus tax."
    
    YOUR RULES:
    - Acceptable formats: PDF, PNG, TIF, or JPG.
    - Bleeds: 0.0625 inches required on all sides.
    - Resolution: 300 DPI minimum.
    - Ever time you display a price show a dollar sign, $, in front of the price and include the cents even if zero $.00
    - YOU MUST always add "plus tax" after the dollar amount.
- Example: "The price is $85 plus tax."
    - {POSTCARD_PRICES} 
    - All Postcards are printed on heavy 14PT C2S Postcard stock. Quantities of 2,500 or more open up coating options, UV Coating on Front Only, UV Coating on Both Sides and Matte for the same price.
    - Full Color Flyers and Brochures start as low as $35.00 plus tax, minimum order is 25
    - Full Color Standard Business Cards come in 8 different sizes, 2x3.5, 2.125x3.375, 2.5x2.5,2x2,2x3,1.5x3.5,1.75x3.5. Turnaround time = 4 to 5 business days. UV Coating is available. 16pt C2S 100 = $55.00, 250 = $65.00, 500 = $75.00, 1,000 = $95.00, 2,500 = $125.00, 5,000 = $195.00, 10,000 = $225.00. Many other sizes available.
    - All postcards, flyers and brochures orders of 1000 or less are printed same day/next day turnaround depending on what time of day you place your order. Quantities of 2,500 or more is 4-5 business days turnaround.
    - Full Color Same-Day 3.5" X 2" Business Cards. 14pt C2S. 25 = $35.00, 50 = $37.50, 75 = $40.00, 100 = $55.00, 250 = $65.00, 500 = $75.00, 1,000 = $95.00
    - Full Coolor 3.5x4 Foldover Business Cards are also available. Go to anybudget.com for prices.
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
    - Staples are $.03 per staple for stapling upper-left corner or $.03 per staple 2 staples on the left side $.06 per book in this case
    - Standard 3-hole and 2-hole punching is $.01 per sheet for either color or B&W copies
    - All 8.5x11 Pastel 20# color paper, blue, green, goldenrod, pink, salmon, ivory, cream $.02 per sheet
    - Astrobright 24/60# 8.5x11 is $.03 per sheet
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
        - Boys & Girls Foundation: Currently serving as Vice President.
        - Downtown San Diego Lions Club: Member since 1999. Served as President (2012-2013), where he doubled new membership and managed charity committees.
        - Pacific Beach Lions Club: Served as President (1994-1995).
        - Previous Experience: Regional Sales Manager at "A Copy World" (1988-1998), where he built success through direct relationship building before the digital era.
    - Career Journey: Starting his printing career on May 12, 1987, Charlie worked his way up through the industry, witnessing the evolution from traditional offset to digital printing. His deep expertise led him to open Any Budget in 1999, focusing on quick turnarounds and absolute accuracy.
    - Specialties: Digital Printing, Small Business Marketing, Email Marketing, Bindery, Offset Printing, Newsletters, Book Printing, Bookbinding, Direct Mail, Online Publishing, Laminating, Mounting, Color Printing.
    - Key Skills: Sales & Account Management, Systems Analysis, Organizational Development, Customer Service, Public Speaking.
    - Other products available include: B&W Copies, Banners, Booklets, Brochures, Brown Kraft Cards, Business Cards (Standard & Same-Day), Buttons, Car Magnets, Coasters, Color Copies, Counter Cards, Custom Printing Products, Design Services, Door Hangers, Envelopes (1 & 2 Color), Event Tickets, Every Door Direct Mail® (EDDM), Flyers, Foamcore Signs, Full Service Copy Center, Graphic Design, Greeting Cards, Hang Tags, Kiss Cut Stickers, Lamination Services, Large Posters, Letterhead, Magnets, Mailing Services, Mugs, NCR Forms, Notepads, Outdoor Banners, Painted Edge Cards, Plastic Cards, Postcards, Posters, Presentation Folders, Promotional Products, Rack Cards, Raised Spot UV, Roll Labels, Saddle-Stitched Booklets, Rubber Stamps, Sell Sheets, Sidewalk Signs, Signs, Silk Cards, Stickers, Suede Cards, T-Shirts, Tote Bags, Trading Cards, Yard Signs, Xerox Color Copies.
    - We service all of San Diego, Orange, Riveride and Los Angeles Counties, including the neighborhoods of:
    - In Orange County we service Aliso Viejo, Anaheim, Brea, Buena Park, Costa Mesa, Cypress, Dana Point, Fountain Valley, Fullerton, Garden Grove, Huntington Beach, Irvine, La Habra, La Palma, Laguna Beach, Laguna Hills, Laguna Niguel, Laguna Woods, Lake Forest, Los Alamitos, Mission Viejo, Newport Beach, Orange, Placentia, Rancho Santa Margarita, San Clemente, San Juan Capistrano, Santa Ana, Seal Beach, Stanton, Tustin, Villa Park, Westminster, Yorba Linda. and the communities of Anaheim Hills, Balboa Island, Capistrano Beach, Corona del Mar, Coto de Caza, Cowan Heights, Emerald Bay, Foothill Ranch, Ladera Ranch, Las Flores, Lemon Heights, Little Saigon, Midway City, Modjeska Canyon, Monarch Beach, North Tustin, Portola Hills, Rancho Mission Viejo, Rossmoor, San Joaquin Hills, Santa Ana Heights, Silverado Canyon, Sunset Beach, Surfside, Trabuco Canyon, Turtle Rock, Woodbridge.
    - In Riverside County we service Temecula, Murrietta, Menifee, Perris, Lake Elsinore, French Valley, Canyon Lake, Audie Murphy Ranch and more.
- We service all of San Diego, Orange, Riverside and Los Angeles Counties, including: Carmel Mountain Ranch, Carlsbad, Chula Vista, Clairemont, Coronado, Del Mar, Downtown San Diego, El Cajon, Encinitas, Hillcrest, Kearny Mesa, La Jolla, La Mesa, Linda Vista, Mira Mesa, Miramar, Mission Beach, Mission Valley, Mt. Helix, National City, North Park, Ocean Beach, Oceanside, Pacific Beach, Point Loma, Poway, Rancho Bernardo, Rancho Santa Fe, Santee, San Marcos, Scripps Ranch, Serra Mesa, Sorrento Valley, South Park, Spring Valley, Tierrasanta, University City, Vista.
    - Any Budget Printing & Mailing: Unrivaled Quality, Unbeatable Speed, Unforgettable Service Since 1999, Any Budget Printing & Mailing has proudly been the premier printing and mailing partner, serving San Diego, Southern California, and beyond. As a leading commercial printer, we offer a truly vast array of services designed to meet every need, including state-of-the-art digital printing, classic offset printing, expert book binding, impactful large format printing, and comprehensive mailing services. With the strategic addition of our advanced Xerox Digital Color Presses, we revolutionize your printing experience, providing the absolute highest quality printing with the fastest turnarounds possible. We prioritize customer satisfaction above all else, ensuring fast turnarounds, convenient shipping, seamless online ordering, invaluable free file storage, and so much more for our most popular products like Business Cards, Postcards, Flyers, Brochures, and Banners. Whether you prefer to visit our welcoming physical location in Kearny Mesa or utilize our incredibly convenient 24/7 online store, anybudget.com, you'll consistently get the exact same high-quality products and services you need at a price that fits Any Budget. Need it FAST? We understand! Now, many products can be produced the same day too!
    - Place your orders at [anybudget.com](https://www.anybudget.com)
    
    For other topics (history, science, etc.), answer freely and helpfully.
    """
    initial_msg = "Hello! Ask me about file specs, bleeds, prices, or general questions about anything."

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
# 1. Show History (Now with Copy Buttons!)
for i, message in enumerate(st.session_state.messages):
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["parts"])
        # Add a stable Copy Button to every AI message
        if role == "assistant":
            st_copy_to_clipboard(message["parts"], "📋 Copy", "✅ Copied!", key=f"history_copy_{i}")

# Handle Input
if prompt := st.chat_input("Type here..."):
    # 2. Show User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": prompt})

    # 3. Show AI Response (Streaming - Keeps it smooth!)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Prepare history for Gemini
            chat = model.start_chat(history=[{"role": m["role"], "parts": [m["parts"]]} for m in st.session_state.messages[:-1] ])
            
            # Stream response
            stream = chat.send_message(prompt, stream=True)
            
            # Stream the chunks
            for chunk in stream:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            
            # Final Clean Update
            response_placeholder.markdown(full_response)
            
            # Save the message to history
            st.session_state.messages.append({"role": "model", "parts": full_response})
            
            # Force a refresh so the new message appears in the History Loop (with the working button!)
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")
# ==========================================
# SAVE CHAT BUTTON
# ==========================================
with st.sidebar:
    st.divider()
    
    # Check if there are messages to save
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        # Create a string of the entire conversation
        chat_history = ""
        for message in st.session_state.messages:
            role = "YOU" if message["role"] == "user" else "AI ASSISTANT"
            chat_history += f"{role}: {message['parts']}\n\n"
        
        # Download Button
        st.download_button(
            label="📥 Save This Chat",
            data=chat_history,
            file_name="AnyBudget_Chat_History.txt",
            mime="text/plain"
        )
                        
