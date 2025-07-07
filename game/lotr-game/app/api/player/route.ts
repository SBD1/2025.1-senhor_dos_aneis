import { NextRequest, NextResponse } from 'next/server'
import { Client } from 'pg'

const client = new Client({
  connectionString: process.env.DATABASE_URL,
})

export async function POST(request: NextRequest) {
  try {
    await client.connect()
    
    const { nome, classe } = await request.json()
    
    // Inserir personagem
    const personagemResult = await client.query(
      'INSERT INTO personagem (nome, vida_maxima, mana_maxima, habilidade, level) VALUES ($1, $2, $3, $4, $5) RETURNING ID_personagem',
      [nome, 100, 100, classe, 1]
    )
    
    const personagemId = personagemResult.rows[0].id_personagem
    
    // Inserir jogador
    await client.query(
      'INSERT INTO jogador (ID_personagem, cenario, tipo_equipamento) VALUES ($1, $2, $3)',
      [personagemId, 1, 'Básico']
    )
    
    // Inserir skills baseado na classe
    const ataqueBase = classe === 'Guerreiro' ? 85 : classe === 'Mago' ? 60 : classe === 'Arqueiro' ? 75 : 50
    await client.query(
      'INSERT INTO skill (ID_jogador, atq) VALUES ($1, $2)',
      [personagemId, ataqueBase]
    )
    
    // Inserir classe específica
    if (classe === 'Guerreiro') {
      await client.query(
        'INSERT INTO guerreiro (id_personagem, atq_Fisico, bloquear_Dano) VALUES ($1, $2, $3)',
        [personagemId, 85, 70]
      )
    } else if (classe === 'Mago') {
      await client.query(
        'INSERT INTO mago (id_personagem, atq_Magico, atq_MultiElemento) VALUES ($1, $2, $3)',
        [personagemId, 80, 70]
      )
    } else if (classe === 'Sacerdote') {
      await client.query(
        'INSERT INTO sacerdote (id_personagem, bencao_Cura, atq_Especial) VALUES ($1, $2, $3)',
        [personagemId, 90, 45]
      )
    } else if (classe === 'Arqueiro') {
      await client.query(
        'INSERT INTO arqueiro (id_personagem, atq_Preciso, atq_Rapido) VALUES ($1, $2, $3)',
        [personagemId, 90, 85]
      )
    }
    
    await client.end()
    
    return NextResponse.json({ success: true, playerId: personagemId })
  } catch (error) {
    console.error('Erro ao criar personagem:', error)
    return NextResponse.json({ error: 'Erro interno do servidor' }, { status: 500 })
  }
}

export async function GET() {
  try {
    await client.connect()
    
    const result = await client.query(`
      SELECT p.*, j.cenario, j.tipo_equipamento, s.atq
      FROM personagem p
      JOIN jogador j ON p.ID_personagem = j.ID_personagem
      LEFT JOIN skill s ON j.ID_personagem = s.ID_jogador
      ORDER BY p.ID_personagem DESC
      LIMIT 10
    `)
    
    await client.end()
    
    return NextResponse.json(result.rows)
  } catch (error) {
    console.error('Erro ao buscar personagens:', error)
    return NextResponse.json({ error: 'Erro interno do servidor' }, { status: 500 })
  }
}