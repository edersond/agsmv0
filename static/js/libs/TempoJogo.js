const TempoJogo = (() => {
    const FATOR_ESCALA = 288; // 1 dia de jogo = 5 min reais
    const ORIGEM_JOGO_UTC = new Date(Date.UTC(2025, 0, 1, 3, 0, 0)); // 1/1/2025 00:00 GMT-3
  
    function agoraJogo() {
      const agora = new Date();
      const deltaMs = agora - ORIGEM_JOGO_UTC;
      const segundosJogo = (deltaMs / 1000) * FATOR_ESCALA;
  
      const dias = Math.floor(segundosJogo / 86400);
      const horas = Math.floor((segundosJogo % 86400) / 3600);
      const minutos = Math.floor((segundosJogo % 3600) / 60);
  
      return { dia: dias, hora: horas, minuto: minutos };
    }
  
    function jogoParaReal(dia, hora, minuto) {
      const segundosJogo = ((dia * 24 + hora) * 60 + minuto) * 60;
      const segundosReais = segundosJogo / FATOR_ESCALA;
      const msReais = segundosReais * 1000;
  
      return new Date(ORIGEM_JOGO_UTC.getTime() + msReais);
    }
  
    function realParaJogo(dataReal) {
      const deltaMs = dataReal - ORIGEM_JOGO_UTC;
      const segundosJogo = (deltaMs / 1000) * FATOR_ESCALA;
  
      const dias = Math.floor(segundosJogo / 86400);
      const horas = Math.floor((segundosJogo % 86400) / 3600);
      const minutos = Math.floor((segundosJogo % 3600) / 60);
  
      return { dia: dias, hora: horas, minuto: minutos };
    }
  
    return { agoraJogo, jogoParaReal, realParaJogo };
  })();
  