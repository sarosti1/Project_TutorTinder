'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function TutorTinder() {
  const [problem, setProblem] = useState('')
  const [suggestedQuestions, setSuggestedQuestions] = useState([])
  const [availableSlots, setAvailableSlots] = useState([])
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [selectedSlot, setSelectedSlot] = useState(null)

  useEffect(() => {
    fetchAvailableSlots()
  }, [])

  const fetchAvailableSlots = async () => {
    try {
      const response = await fetch('http://localhost:5000/available_slots')
      const data = await response.json()
      setAvailableSlots(data)
    } catch (error) {
      console.error('Error fetching available slots:', error)
    }
  }

  const suggestQuestions = async () => {
    try {
      const response = await fetch('http://localhost:5000/suggest_questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ problem }),
      })
      const data = await response.json()
      setSuggestedQuestions(data.questions)
    } catch (error) {
      console.error('Error suggesting questions:', error)
    }
  }

  const bookTutor = async () => {
    if (!selectedSlot) {
      alert('Please select a time slot')
      return
    }
    try {
      const response = await fetch('http://localhost:5000/book_tutor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          email,
          slot: selectedSlot,
        }),
      })
      const data = await response.json()
      alert(data.message)
    } catch (error) {
      console.error('Error booking tutor:', error)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Welcome to Tutor Tinder</h1>
      <p className="mb-8">Connecting students with the perfect tutors!</p>

      <Card className="mb-8">
        <CardHeader>
          <CardTitle>What's your question?</CardTitle>
        </CardHeader>
        <CardContent>
          <Textarea
            value={problem}
            onChange={(e) => setProblem(e.target.value)}
            placeholder="Enter your problem here"
            className="mb-4"
          />
          <Button onClick={suggestQuestions}>Get Suggested Questions</Button>
          {suggestedQuestions.length > 0 && (
            <div className="mt-4">
              <h3 className="font-bold mb-2">Suggested Questions:</h3>
              <ul className="list-disc pl-5">
                {suggestedQuestions.map((question, index) => (
                  <li key={index}>{question}</li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>

      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Available Tutor Slots</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {availableSlots.map((slot) => (
              <Button
                key={slot.datetime}
                onClick={() => setSelectedSlot(slot)}
                variant={selectedSlot === slot ? "default" : "outline"}
              >
                {slot.tutor_name} - {slot.subject}
                <br />
                {new Date(slot.datetime).toLocaleString()}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Book Your Tutor</CardTitle>
        </CardHeader>
        <CardContent>
          <Input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Your Name"
            className="mb-4"
          />
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Your Email"
            className="mb-4"
          />
          <Button onClick={bookTutor}>Book Tutor</Button>
        </CardContent>
      </Card>
    </div>
  )
}

