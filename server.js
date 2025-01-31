require("dotenv").config();
const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

async function generateResponse(message) {
    try {
        const response = await axios.post(
            `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GEMINI_API_KEY}`,
            {
                contents: [
                    {
                        role: "user",
                        parts: [{ text: `Tum ek friendly, caring, aur masti bhari ladki ho. Tum pyaar bhari aur cute baatein karti ho. User ka message: "${message}"` }]
                    }
                ]
            }
        );

        return response.data.candidates[0].content.parts[0].text;
    } catch (error) {
        throw new Error(error.message);
    }
}

// Handle both GET and POST requests
app.get("/chat", async (req, res) => {
    const message = req.query.message;
    if (!message) {
        return res.status(400).json({ error: "Message parameter is required" });
    }

    try {
        const reply = await generateResponse(message);
        res.json({ reply });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post("/chat", async (req, res) => {
    const { message } = req.body;
    if (!message) {
        return res.status(400).json({ error: "Message is required" });
    }

    try {
        const reply = await generateResponse(message);
        res.json({ reply });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = app;