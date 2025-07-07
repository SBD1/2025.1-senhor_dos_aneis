"use client"

import React from "react"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Sword,
  Shield,
  Wand2,
  Target,
  Heart,
  Zap,
  MapPin,
  Package,
  Users,
  Swords,
  Crown,
  Gem,
  Volume2,
  VolumeX,
} from "lucide-react"

// Tipos do jogo
interface Player {
  id: number
  nome: string
  classe: "Guerreiro" | "Mago" | "Sacerdote" | "Arqueiro"
  vida: number
  vidaMaxima: number
  mana: number
  manaMaxima: number
  level: number
  cenario: number
  ataque: number
  defesa: number
  xp: number
}

interface Cenario {
  id: number
  nome: string
  descricao: string
  clima: string
  norte?: number
  sul?: number
  leste?: number
  oeste?: number
  npcs: NPC[]
  criaturas: Criatura[]
  itens: Item[]
}

interface NPC {
  id: number
  nome: string
  dialogo: string
  tipo: "quest" | "comerciante" | "guia"
  itens?: Item[]
}

interface Criatura {
  id: number
  nome: string
  vida: number
  ataque: number
  xp: number
  dificuldade: string
}

interface Item {
  id: number
  nome: string
  tipo: "arma" | "armadura" | "consumivel" | "especial"
  valor: number
  peso: number
}

// Dados do jogo
const cenarios: Cenario[] = [
  {
    id: 1,
    nome: "Acampamento Élfico",
    descricao:
      "Um refúgio pacífico dos elfos, com tendas douradas e fogueiras acolhedoras. O ar está perfumado com ervas élficas.",
    clima: "Amanhecer dourado",
    leste: 2,
    npcs: [
      {
        id: 1,
        nome: "Erestor, Lorde Élfico",
        dialogo: "Aventureiro, ouvi rumores sobre anéis perdidos em Eregion. Você aceita esta missão perigosa?",
        tipo: "quest",
      },
      {
        id: 2,
        nome: "Lindir, o Curandeiro",
        dialogo: "Minhas poções podem salvar sua vida nas ruínas sombrias. Leve algumas!",
        tipo: "comerciante",
        itens: [{ id: 1, nome: "Poção de Cura Élfica", tipo: "consumivel", valor: 50, peso: 0.5 }],
      },
      {
        id: 3,
        nome: "Glorfindel, o Mercador",
        dialogo: "Armas élficas são sua melhor defesa contra os horrores de Eregion.",
        tipo: "comerciante",
        itens: [{ id: 2, nome: "Espada Élfica", tipo: "arma", valor: 200, peso: 2.5 }],
      },
    ],
    criaturas: [],
    itens: [],
  },
  {
    id: 2,
    nome: "Estrada para Eregion",
    descricao: "Uma estrada antiga e perigosa que leva às ruínas de Eregion. Neblina densa obscurece a visão.",
    clima: "Cinzento e nebuloso",
    oeste: 1,
    leste: 3,
    npcs: [],
    criaturas: [{ id: 4, nome: "Lobo Selvagem", vida: 45, ataque: 25, xp: 150, dificuldade: "Fácil" }],
    itens: [],
  },
  {
    id: 3,
    nome: "Portões de Ost-in-Edhil",
    descricao: "Os portões arruinados da antiga cidade élfica. Sombras dançam entre as pedras quebradas.",
    clima: "Sombrio e tempestuoso",
    oeste: 2,
    leste: 4,
    npcs: [],
    criaturas: [
      { id: 5, nome: "Orc Errante", vida: 80, ataque: 35, xp: 400, dificuldade: "Média" },
      { id: 6, nome: "Espectro Élfico", vida: 90, ataque: 40, xp: 500, dificuldade: "Média" },
    ],
    itens: [],
  },
  {
    id: 4,
    nome: "Salões das Forjas",
    descricao: "O coração das antigas forjas élficas. Ecos de martelos fantasmas ainda ressoam pelos corredores.",
    clima: "Luz fantasmagórica",
    oeste: 3,
    norte: 5,
    leste: 6,
    sul: 7,
    npcs: [],
    criaturas: [{ id: 7, nome: "Balrog Menor", vida: 300, ataque: 80, xp: 2000, dificuldade: "Difícil" }],
    itens: [],
  },
  {
    id: 5,
    nome: "Forja Principal",
    descricao: "A grande forja onde os anéis foram criados. Brasas vermelhas ainda brilham nas profundezas.",
    clima: "Chamas dançantes",
    sul: 4,
    npcs: [],
    criaturas: [],
    itens: [{ id: 7, nome: "Anel da Proteção", tipo: "especial", valor: 1000, peso: 0.1 }],
  },
  {
    id: 6,
    nome: "Câmara dos Segredos",
    descricao: "Uma câmara misteriosa cheia de espelhos antigos que refletem memórias do passado.",
    clima: "Espelhos brilhantes",
    oeste: 4,
    npcs: [],
    criaturas: [{ id: 8, nome: "Sombra Antiga", vida: 60, ataque: 30, xp: 350, dificuldade: "Média" }],
    itens: [{ id: 8, nome: "Anel da Invisibilidade Menor", tipo: "especial", valor: 1000, peso: 0.1 }],
  },
  {
    id: 7,
    nome: "Torre do Observatório",
    descricao: "Uma torre alta com vista panorâmica de toda Eregion. Ventos fortes sopram constantemente.",
    clima: "Vista panorâmica",
    norte: 4,
    npcs: [],
    criaturas: [
      { id: 9, nome: "Nazgûl Menor", vida: 250, ataque: 70, xp: 1500, dificuldade: "Difícil" },
      { id: 10, nome: "Capitão Nazgûl", vida: 400, ataque: 100, xp: 5000, dificuldade: "Extrema" },
    ],
    itens: [{ id: 9, nome: "Anel da Compreensão", tipo: "especial", valor: 1000, peso: 0.1 }],
  },
]

const classesInfo = {
  Guerreiro: { icon: Sword, cor: "bg-red-500", descricao: "Especialista em combate físico" },
  Mago: { icon: Wand2, cor: "bg-blue-500", descricao: "Mestre dos elementos" },
  Sacerdote: { icon: Shield, cor: "bg-yellow-500", descricao: "Curandeiro e protetor" },
  Arqueiro: { icon: Target, cor: "bg-green-500", descricao: "Combate à distância" },
}

export default function LotrGame() {
  const [gameState, setGameState] = useState<'menu' | 'character-creation' | 'playing' | 'battle' | 'victory'>('menu')
  const [player, setPlayer] = useState<Player | null>(null)
  const [currentCenario, setCurrentCenario] = useState<Cenario>(cenarios[0])
  const [gameLog, setGameLog] = useState<string[]>(['Bem-vindo aos Anéis Perdidos de Eregion!'])
  const [selectedNPC, setSelectedNPC] = useState<NPC | null>(null)
  const [battleTarget, setBattleTarget] = useState<Criatura | null>(null)
  const [inventory, setInventory] = useState<Item[]>([])
  const [musicEnabled, setMusicEnabled] = useState(true)
  const audioRef = useRef<HTMLAudioElement>(null)

  // Música de fundo
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = 0.3
      if (musicEnabled) {
        audioRef.current.play().catch(() => {})
      } else {
        audioRef.current.pause()
      }
    }
  }, [musicEnabled, gameState])

  const addToLog = (message: string) => {
    setGameLog(prev => [...prev.slice(-9), message])
  }

  const createCharacter = async (nome: string, classe: Player['classe']) => {
    try {
      // Tentar salvar no banco de dados
      const response = await fetch('/api/player', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome, classe }),
      })
      
      if (response.ok) {
        const data = await response.json()
        
        const baseStats = {
          Guerreiro: { vida: 120, mana: 50, ataque: 85, defesa: 70 },
          Mago: { vida: 80, mana: 150, ataque: 60, defesa: 40 },
          Sacerdote: { vida: 100, mana: 120, ataque: 50, defesa: 60 },
          Arqueiro: { vida: 90, mana: 80, ataque: 75, defesa: 50 }
        }

        const stats = baseStats[classe]
        const newPlayer: Player = {
          id: data.playerId || 1,
          nome,
          classe,
          vida: stats.vida,
          vidaMaxima: stats.vida,
          mana: stats.mana,
          manaMaxima: stats.mana,
          level: 1,
          cenario: 1,
          ataque: stats.ataque,
          defesa: stats.defesa,
          xp: 0
        }

        setPlayer(newPlayer)
        setCurrentCenario(cenarios[0])
        setGameState('playing')
        addToLog(`${nome}, o ${classe}, inicia sua jornada em Eregion! (Salvo no banco)`)
      } else {
        throw new Error('Falha ao salvar no banco')
      }
    } catch (error) {
      console.error('Erro ao conectar com banco:', error)
      addToLog('Conectando em modo offline...')
      
      // Fallback para modo offline
      const baseStats = {
        Guerreiro: { vida: 120, mana: 50, ataque: 85, defesa: 70 },
        Mago: { vida: 80, mana: 150, ataque: 60, defesa: 40 },
        Sacerdote: { vida: 100, mana: 120, ataque: 50, defesa: 60 },
        Arqueiro: { vida: 90, mana: 80, ataque: 75, defesa: 50 }
      }

      const stats = baseStats[classe]
      const newPlayer: Player = {
        id: Math.floor(Math.random() * 1000),
        nome,
        classe,
        vida: stats.vida,
        vidaMaxima: stats.vida,
        mana: stats.mana,
        manaMaxima: stats.mana,
        level: 1,
        cenario: 1,
        ataque: stats.ataque,
        defesa: stats.defesa,
        xp: 0
      }

      setPlayer(newPlayer)
      setCurrentCenario(cenarios[0])
      setGameState('playing')
      addToLog(`${nome}, o ${classe}, inicia sua jornada em Eregion! (Modo offline)`)
    }
  }

  const movePlayer = (direction: 'norte' | 'sul' | 'leste' | 'oeste') => {
    const nextCenarioId = currentCenario[direction]
    if (nextCenarioId) {
      const nextCenario = cenarios.find(c => c.id === nextCenarioId)
      if (nextCenario) {
        setCurrentCenario(nextCenario)
        if (player) {
          setPlayer({ ...player, cenario: nextCenarioId })
        }
        addToLog(`Você se move para ${direction} e chega em: ${nextCenario.nome}`)
        
        // Chance de encontro aleatório
        if (nextCenario.criaturas.length > 0 && Math.random() < 0.3) {
          const randomCreature = nextCenario.criaturas[Math.floor(Math.random() * nextCenario.criaturas.length)]
          addToLog(`Um ${randomCreature.nome} aparece!`)
        }
      }
    } else {
      addToLog('Não há caminho nesta direção.')
    }
  }

  const startBattle = (creature: Criatura) => {
    setBattleTarget(creature)
    setGameState('battle')
    addToLog(`Batalha iniciada contra ${creature.nome}!`)
  }

  const executeBattle = () => {
    if (!player || !battleTarget) return

    const playerDamage = player.ataque + Math.floor(Math.random() * 20) - 10
    const creatureDamage = battleTarget.ataque + Math.floor(Math.random() * 15) - 7

    const finalPlayerDamage = Math.max(1, playerDamage)
    const finalCreatureDamage = Math.max(1, creatureDamage - player.defesa / 2)

    // Aplicar dano
    const newCreatureLife = Math.max(0, battleTarget.vida - finalPlayerDamage)
    const newPlayerLife = Math.max(0, player.vida - finalCreatureDamage)

    if (newCreatureLife <= 0) {
      // Vitória do jogador
      const newXP = player.xp + battleTarget.xp
      const newLevel = Math.floor(newXP / 1000) + 1
      
      setPlayer({
        ...player,
        xp: newXP,
        level: newLevel,
        vida: newPlayerLife
      })

      // Remover criatura do cenário
      const updatedCenario = {
        ...currentCenario,
        criaturas: currentCenario.criaturas.filter(c => c.id !== battleTarget.id)
      }
      setCurrentCenario(updatedCenario)

      addToLog(`Você derrotou ${battleTarget.nome}! Ganhou ${battleTarget.xp} XP.`)
      if (newLevel > player.level) {
        addToLog(`Parabéns! Você subiu para o nível ${newLevel}!`)
      }
      
      setGameState('playing')
      setBattleTarget(null)
    } else if (newPlayerLife <= 0) {
      // Derrota do jogador
      addToLog('Você foi derrotado! Fim de jogo.')
      setGameState('menu')
    } else {
      // Batalha continua
      setBattleTarget({ ...battleTarget, vida: newCreatureLife })
      setPlayer({ ...player, vida: newPlayerLife })
      addToLog(`Você causou ${finalPlayerDamage} de dano. ${battleTarget.nome} causou ${finalCreatureDamage} de dano.`)
    }
  }

  const talkToNPC = (npc: NPC) => {
    setSelectedNPC(npc)
    addToLog(`${npc.nome}: "${npc.dialogo}"`)
  }

  const collectItem = (item: Item) => {
    setInventory(prev => [...prev, item])
    const updatedCenario = {
      ...currentCenario,
      itens: currentCenario.itens.filter(i => i.id !== item.id)
    }
    setCurrentCenario(updatedCenario)
    addToLog(`Você coletou: ${item.nome}`)

    // Verificar vitória (todos os 3 anéis)
    const aneis = ['Anel da Proteção', 'Anel da Invisibilidade Menor', 'Anel da Compreensão']
    const aneisColetados = inventory.filter(i => aneis.includes(i.nome)).length + (aneis.includes(item.nome) ? 1 : 0)
    
    if (aneisColetados === 3) {
      setGameState('victory')
      addToLog('Parabéns! Você coletou todos os três anéis perdidos de Eregion!')
    }
  }

  const CharacterCreation = () => {
    const [nome, setNome] = useState('')
    const [classeEscolhida, setClasseEscolhida] = useState<Player['classe'] | null>(null)

    return (
      <div className="min-h-screen bg-gradient-to-b from-amber-900 via-amber-800 to-amber-900 flex items-center justify-center p-4">
        <Card className="w-full max-w-2xl bg-amber-50 border-amber-200">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl text-amber-900">Criação de Personagem</CardTitle>
            <CardDescription>Escolha seu nome e classe para começar sua jornada</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-amber-900 mb-2">Nome do Personagem</label>
              <input
                type="text"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                className="w-full p-3 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500"
                placeholder="Digite o nome do seu personagem"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-amber-900 mb-4">Escolha sua Classe</label>
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(classesInfo).map(([classe, info]) => {
                  const IconComponent = info.icon
                  return (
                    <Card
                      key={classe}
                      className={`cursor-pointer transition-all hover:scale-105 ${
                        classeEscolhida === classe ? 'ring-2 ring-amber-500 bg-amber-100' : 'hover:bg-amber-50'
                      }`}
                      onClick={() => setClasseEscolhida(classe as Player['classe'])}
                    >
                      <CardContent className="p-4 text-center">
                        <div className={`w-12 h-12 ${info.cor} rounded-full flex items-center justify-center mx-auto mb-2`}>
                          <IconComponent className="w-6 h-6 text-white" />
                        </div>
                        <h3 className="font-bold text-amber-900">{classe}</h3>
                        <p className="text-sm text-amber-700">{info.descricao}</p>
                      </CardContent>
                    </Card>
                  )
                })}
              </div>
            </div>

            <div className="flex gap-4">
              <Button
                onClick={() => setGameState('menu')}
                variant="outline"
                className="flex-1"
              >
                Voltar
              </Button>
              <Button
                onClick={() => nome && classeEscolhida && createCharacter(nome, classeEscolhida)}
                disabled={!nome || !classeEscolhida}
                className="flex-1 bg-amber-600 hover:bg-amber-700"
              >
                Começar Aventura
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const GameInterface = () => {
    if (!player) return null

    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 text-white">
        <div className="container mx-auto p-4">
          {/* Header com informações do jogador */}
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center gap-4">
              <div className={`w-12 h-12 ${classesInfo[player.classe].cor} rounded-full flex items-center justify-center`}>
                {React.createElement(classesInfo[player.classe].icon, { className: "w-6 h-6 text-white" })}
              </div>
              <div>
                <h1 className="text-2xl font-bold">{player.nome}</h1>
                <p className="text-slate-300">{player.classe} - Nível {player.level}</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Button
                onClick={() => setMusicEnabled(!musicEnabled)}
                variant="outline"
                size="sm"
              >
                {musicEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
              </Button>
              <Button
                onClick={() => setGameState('menu')}
                variant="outline"
                size="sm"
              >
                Menu Principal
              </Button>
            </div>
          </div>

          {/* Status do jogador */}
          <div className="grid grid-cols-4 gap-4 mb-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Heart className="w-4 h-4 text-red-500" />
                  <span className="text-sm">Vida</span>
                </div>
                <Progress value={(player.vida / player.vidaMaxima) * 100} className="mb-1" />
                <span className="text-xs text-slate-400">{player.vida}/{player.vidaMaxima}</span>
              </CardContent>
            </Card>
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Zap className="w-4 h-4 text-blue-500" />
                  <span className="text-sm">Mana</span>
                </div>
                <Progress value={(player.mana / player.manaMaxima) * 100} className="mb-1" />
                <span className="text-xs text-slate-400">{player.mana}/{player.manaMaxima}</span>
              </CardContent>
            </Card>
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Sword className="w-4 h-4 text-orange-500" />
                  <span className="text-sm">Ataque</span>
                </div>
                <span className="text-lg font-bold">{player.ataque}</span>
              </CardContent>
            </Card>
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Crown className="w-4 h-4 text-yellow-500" />
                  <span className="text-sm">XP</span>
                </div>
                <span className="text-lg font-bold">{player.xp}</span>
              </CardContent>
            </Card>
          </div>

          <div className="grid grid-cols-3 gap-6">
            {/* Cenário atual */}
            <div className="col-span-2">
              <Card className="bg-slate-800 border-slate-700 mb-4">
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-5 h-5 text-green-500" />
                    <CardTitle>{currentCenario.nome}</CardTitle>
                  </div>
                  <CardDescription className="text-slate-300">
                    {currentCenario.descricao}
                  </CardDescription>
                  <Badge variant="outline" className="w-fit">
                    {currentCenario.clima}
                  </Badge>
                </CardHeader>
                <CardContent>
                  {/* Controles de movimento */}
                  <div className="grid grid-cols-3 gap-2 mb-4 max-w-48 mx-auto">
                    <div></div>
                    <Button
                      onClick={() => movePlayer('norte')}
                      disabled={!currentCenario.norte}
                      variant="outline"
                      size="sm"
                    >
                      ↑ Norte
                    </Button>
                    <div></div>
                    <Button
                      onClick={() => movePlayer('oeste')}
                      disabled={!currentCenario.oeste}
                      variant="outline"
                      size="sm"
                    >
                      ← Oeste
                    </Button>
                    <div></div>
                    <Button
                      onClick={() => movePlayer('leste')}
                      disabled={!currentCenario.leste}
                      variant="outline"
                      size="sm"
                    >
                      Leste →
                    </Button>
                    <div></div>
                    <Button
                      onClick={() => movePlayer('sul')}
                      disabled={!currentCenario.sul}
                      variant="outline"
                      size="sm"
                    >
                      ↓ Sul
                    </Button>
                    <div></div>
                  </div>

                  {/* NPCs */}
                  {currentCenario.npcs.length > 0 && (
                    <div className="mb-4">
                      <h3 className="flex items-center gap-2 font-semibold mb-2">
                        <Users className="w-4 h-4" />
                        NPCs
                      </h3>
                      <div className="space-y-2">
                        {currentCenario.npcs.map(npc => (
                          <Button
                            key={npc.id}
                            onClick={() => talkToNPC(npc)}
                            variant="outline"
                            className="w-full justify-start"
                          >
                            {npc.nome}
                          </Button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Criaturas */}
                  {currentCenario.criaturas.length > 0 && (
                    <div className="mb-4">
                      <h3 className="flex items-center gap-2 font-semibold mb-2">
                        <Swords className="w-4 h-4" />
                        Criaturas
                      </h3>
                      <div className="space-y-2">
                        {currentCenario.criaturas.map(creature => (
                          <div key={creature.id} className="flex items-center justify-between p-2 bg-slate-700 rounded">
                            <div>
                              <span className="font-medium">{creature.nome}</span>
                              <Badge variant="outline" className="ml-2">
                                {creature.dificuldade}
                              </Badge>
                            </div>
                            <Button
                              onClick={() => startBattle(creature)}
                              size="sm"
                              variant="destructive"
                            >
                              Atacar
                            </Button>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Itens */}
                  {currentCenario.itens.length > 0 && (
                    <div>
                      <h3 className="flex items-center gap-2 font-semibold mb-2">
                        <Gem className="w-4 h-4" />
                        Itens
                      </h3>
                      <div className="space-y-2">
                        {currentCenario.itens.map(item => (
                          <div key={item.id} className="flex items-center justify-between p-2 bg-slate-700 rounded">
                            <span className="font-medium">{item.nome}</span>
                            <Button
                              onClick={() => collectItem(item)}
                              size="sm"
                              variant="outline"
                            >
                              Coletar
                            </Button>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Painel lateral */}
            <div>
              <Tabs defaultValue="log" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="log">Log</TabsTrigger>
                  <TabsTrigger value="inventory">
                    <Package className="w-4 h-4 mr-1" />
                    Inventário
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="log">
                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-lg">Log do Jogo</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ScrollArea className="h-64">
                        <div className="space-y-2">
                          {gameLog.map((log, index) => (
                            <p key={index} className="text-sm text-slate-300">
                              {log}
                            </p>
                          ))}
                        </div>
                      </ScrollArea>
                    </CardContent>
                  </Card>
                </TabsContent>
                
                <TabsContent value="inventory">
                  <Card className="bg-slate-800 border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-lg">Inventário</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ScrollArea className="h-64">
                        {inventory.length === 0 ? (
                          <p className="text-slate-400 text-sm">Inventário vazio</p>
                        ) : (
                          <div className="space-y-2">
                            {inventory.map((item, index) => (
                              <div key={index} className="p-2 bg-slate-700 rounded">
                                <div className="font-medium">{item.nome}</div>
                                <div className="text-xs text-slate-400">
                                  {item.tipo} • Peso: {item.peso}kg
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </ScrollArea>
                    </CardContent>
                  </Card>
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </div>

        {/* Áudio de fundo */}
        <audio ref={audioRef} loop>
          <source src="/placeholder-audio.mp3" type="audio/mpeg" />
        </audio>
      </div>
    )
  }

  const BattleInterface = () => {
    if (!player || !battleTarget) return null

    return (
      <div className="min-h-screen bg-gradient-to-b from-red-900 via-red-800 to-red-900 text-white">
        <div className="container mx-auto p-4">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-4">Batalha!</h1>
            <p className="text-xl">Você está enfrentando {battleTarget.nome}</p>
          </div>

          <div className="grid grid-cols-2 gap-8 mb-8">
            {/* Jogador */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {React.createElement(classesInfo[player.classe].icon, { className: "w-6 h-6" })}
                  {player.nome}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span>Vida</span>
                      <span>{player.vida}/{player.vidaMaxima}</span>
                    </div>
                    <Progress value={(player.vida / player.vidaMaxima) * 100} />
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span>Mana</span>
                      <span>{player.mana}/{player.manaMaxima}</span>
                    </div>
                    <Progress value={(player.mana / player.manaMaxima) * 100} />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="text-sm text-slate-400">Ataque</span>
                      <p className="font-bold">{player.ataque}</p>
                    </div>
                    <div>
                      <span className="text-sm text-slate-400">Defesa</span>
                      <p className="font-bold">{player.defesa}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Criatura */}
            <Card className="bg-red-800 border-red-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Swords className="w-6 h-6" />
                  {battleTarget.nome}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span>Vida</span>
                      <span>{battleTarget.vida}</span>
                    </div>
                    <Progress value={(battleTarget.vida / 100) * 100} className="bg-red-600" />
                  </div>
                  <div>
                    <span className="text-sm text-red-300">Ataque</span>
                    <p className="font-bold">{battleTarget.ataque}</p>
                  </div>
                  <Badge variant="outline" className="w-fit">
                    {battleTarget.dificuldade}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="text-center space-y-4">
            <Button
              onClick={executeBattle}
              size="lg"
              className="bg-red-600 hover:bg-red-700"
            >
              Atacar!
            </Button>
            <div>
              <Button
                onClick={() => setGameState('playing')}
                variant="outline"
                size="sm"
              >
                Fugir
              </Button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const VictoryScreen = () => {
    return (
      <div className="min-h-screen bg-gradient-to-b from-yellow-900 via-yellow-800 to-yellow-900 text-white flex items-center justify-center">
        <Card className="w-full max-w-2xl bg-yellow-50 border-yellow-200 text-yellow-900">
          <CardHeader className="text-center">
            <CardTitle className="text-4xl mb-4">🎉 Vitória! 🎉</CardTitle>
            <CardDescription className="text-xl">
              Parabéns! Você coletou todos os três anéis perdidos de Eregion!
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center space-y-6">
            <div className="flex justify-center gap-4">
              <div className="text-center">
                <div className="w-16 h-16 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-2">
                  <Crown className="w-8 h-8 text-white" />
                </div>
                <p className="text-sm">Anel da Proteção</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-2">
                  <Crown className="w-8 h-8 text-white" />
                </div>
                <p className="text-sm">Anel da Invisibilidade</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-2">
                  <Crown className="w-8 h-8 text-white" />
                </div>
                <p className="text-sm">Anel da Compreensão</p>
              </div>
            </div>
            <div className="space-y-2">
              <p>Você completou sua missão com sucesso!</p>
              <p className="text-sm text-yellow-700">
                Os anéis perdidos de Eregion foram recuperados e a paz foi restaurada.
              </p>
            </div>
            <Button
              onClick={() => setGameState('menu')}
              className="bg-yellow-600 hover:bg-yellow-700"
            >
              Voltar ao Menu Principal
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Renderização principal
  return (
    <div>
      {gameState === 'menu' && (
        <div className="min-h-screen bg-gradient-to-b from-amber-900 via-amber-800 to-amber-900 flex items-center justify-center p-4">
          <Card className="w-full max-w-md bg-amber-50 border-amber-200">
            <CardHeader className="text-center">
              <CardTitle className="text-4xl text-amber-900 mb-2">O Senhor dos Anéis</CardTitle>
              <CardDescription className="text-xl text-amber-700">
                Os Anéis Perdidos de Eregion
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button
                onClick={() => setGameState('character-creation')}
                className="w-full bg-amber-600 hover:bg-amber-700"
                size="lg"
              >
                Nova Aventura
              </Button>
              <Button
                onClick={() => setGameState('playing')}
                variant="outline"
                className="w-full"
                size="lg"
              >
                Continuar Jogo
              </Button>
            </CardContent>
          </Card>
        </div>
      )}

      {gameState === 'character-creation' && <CharacterCreation />}
      {gameState === 'playing' && <GameInterface />}
      {gameState === 'battle' && <BattleInterface />}
      {gameState === 'victory' && <VictoryScreen />}

      {/* Modal de NPC */}
      {selectedNPC && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-md bg-slate-800 border-slate-700 text-white">
            <CardHeader>
              <CardTitle>{selectedNPC.nome}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-slate-300">{selectedNPC.dialogo}</p>
              
              {selectedNPC.tipo === 'comerciante' && selectedNPC.itens && (
                <div>
                  <h4 className="font-semibold mb-2">Itens disponíveis:</h4>
                  <div className="space-y-2">
                    {selectedNPC.itens.map(item => (
                      <div key={item.id} className="flex justify-between items-center p-2 bg-slate-700 rounded">
                        <span>{item.nome}</span>
                        <Button
                          onClick={() => {
                            collectItem(item)
                            setSelectedNPC(null)
                          }}
                          size="sm"
                        >
                          Comprar ({item.valor} moedas)
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              <Button
                onClick={() => setSelectedNPC(null)}
                className="w-full"
              >
                Fechar
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
