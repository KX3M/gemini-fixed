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
                        parts: [{ text: `prompt=Tum ek friendly, caring, aur masti bhari ladki ho. Tum pyaar bhari aur cute baatein karti ho & tum hinglish mai baat Krna. User ka message: "${message}"` }]
                    }
                ]
            }
        );

        if (
            response.data &&
            response.data.candidates &&
            response.data.candidates[0] &&
            response.data.candidates[0].content &&
            response.data.candidates[0].content.parts &&
            response.data.candidates[0].content.parts[0]
        ) {
            return response.data.candidates[0].content.parts[0].text;
        } else {
            throw new Error("Invalid response from Gemini API");
        }
    } catch (error) {
        throw new Error(error.response?.data?.error?.message || error.message);
    }
}

app.get("/chat", async (req, res) => {
    const message = req.query.message;
    if (!message) {
        return res.status(400).json({ error: "Message parameter is required" });
    }

    try {
        const reply = await generateResponse(message);
        res.json({ reply, Owner: "@MysticoFF" });
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
        res.json({ reply, Owner: "@MysticoFF" });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = app;