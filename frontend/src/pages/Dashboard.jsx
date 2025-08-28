import { useEffect, useState } from 'react'
import { api, setAuth } from '../services/api'
import { getToken } from '../services/auth'
import Nav from '../components/Nav'

export default function Dashboard() {
  const [meals, setMeals] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const t = getToken()
    setAuth(t)
    api.get('/meals').then(res => setMeals(res.data.items)).finally(()=>setLoading(false))
  }, [])

  return (
    <div className="min-h-screen">
      <Nav/>
      <div className="max-w-5xl mx-auto p-4">
        <h1 className="text-2xl font-semibold mb-4">Your history</h1>
        {loading ? <div>Loading…</div> : (
          <div className="grid md:grid-cols-2 gap-4">
            {meals.map(m => (
              <div key={m.id} className="card">
                <div className="font-medium mb-2">{new Date(m.timestamp).toLocaleString()}</div>
                {m.image_path && <img src={`file://${m.image_path}`} alt="" className="rounded-xl mb-3" />}
                <div className="text-sm text-gray-700 mb-2">Status: <b>{m.status}</b></div>
                {m.nutrition && (
                  <div className="text-sm">
                    <div>Calories: {m.nutrition.calories}</div>
                    <div>Protein: {m.nutrition.protein_g}g</div>
                    <div>Carbs: {m.nutrition.carbs_g}g</div>
                    <div>Fat: {m.nutrition.fat_g}g</div>
                  </div>
                )}
                {m.notes && <div className="text-sm mt-2 italic">“{m.notes}”</div>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
