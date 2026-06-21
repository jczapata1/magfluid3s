module integration

    contains
    
!--------------------------------------------------------------------------------------------------------------------------------------------------------------

    !! Stratonovich–Heun Algorithm
    subroutine stratonovich_heun(Mui, Emi, Eni, Zi, SHi, S0i, Ha, Hb, HK, Ca, Cb, dt)

        ! Perform the Stratonovich–Heun algorithm.
        !
        ! Input:   
        ! -              Mui (real*8): ith-Magnetic Moment (Magnitude)        
        ! - Emi (real*8, array[3, 1]): ith-Magnetic Moment (Vector)
        ! - Eni (real*8, array[3, 1]): ith-Easy Axis
        ! -               Zi (real*8): ith-Drag Cointicient          
        ! -              SHi (real*8): ith-Thermal Field Standard Deviation
        ! -              S0i (real*8): ith-Thermal Torque Standard Deviation        
        ! -  Ha (real*8, array[3, 1]): Magnetic Field -> H = H(t) 
        ! -  Hb (real*8, array[3, 1]): Magnetic Field -> H = H(t+dt)  
        ! -               HK (real*8): Anisotropic Field Amplitude 
        ! -               Ca (real*8): Damping Constant   
        ! -               Cb (real*8): Damping Constant         
        ! -               dt (real*8): Integration Time         
        !
        ! Output:  
        ! - None     
        !
        ! Used by:
        ! - llg-t.integration.evolution

        use constants, only: MU0
        use math, only: rv_normal, dot_prod, cross_prod 
        real*8, intent(in)    :: Mui, Zi, SHi, S0i, Ha(0:2), Hb(0:2), HK, Ca, Cb, dt
        real*8, intent(inout) :: Emi(0:2), Eni(0:2)
        real*8                :: Emi_e(0:2), WH(0:2), Hint(0:2), A(0:2), A_e(0:2), BWH(0:2), BWH_e(0:2)
        real*8                :: Eni_e(0:2), W0(0:2), Oint(0:2), C(0:2), C_e(0:2), DW0(0:2), DW0_e(0:2)

        ! Thermal Noise
        WH = rv_normal(SHi)  
        W0 = rv_normal(S0i)  
        
        ! Euler Predictor   
        Hint  = Ha + HK*dot_prod(Emi, Eni)*Eni                                              ! Hint(m,n,t) 
        A     = -Ca*cross_prod(Emi, Hint) - Cb*cross_prod(Emi, cross_prod(Emi, Hint))       ! A(m,n,t) 
        BWH   = -Ca*cross_prod(Emi, WH) - Cb*cross_prod(Emi, cross_prod(Emi, WH))           ! B(m,t)*WH
        Emi_e = Emi + A*dt + BWH                                                            ! m + A(m,n,t)*dt + B(m,t)*WH 
        Emi_e = Emi_e / sqrt(dot_prod(Emi_e, Emi_e))                                        ! me/|me|

        Oint  = -MU0*Mui*HK * dot_prod(Emi, Eni) * cross_prod(Emi, Eni)                     ! Oint(m,n,t)
        C     = -(1.0/Zi) * cross_prod(Eni, Oint)                                           ! C(m,n,t)
        DW0   = -(1.0/Zi) * cross_prod(Eni, W0)                                             ! D(n,t)*W0
        Eni_e = Eni + C*dt + DW0                                                            ! n + C(m,n,t)*dt + D(n,t)*W0 
        Eni_e = Eni_e / sqrt(dot_prod(Eni_e, Eni_e))                                        ! ne/|ne|     

        ! Heun Predictor 
        Hint  = Hb + HK*dot_prod(Emi_e, Eni_e)*Eni_e                                        ! Hint(me,ne,t+dt)
        A_e   = -Ca*cross_prod(Emi_e, Hint) - Cb*cross_prod(Emi_e, cross_prod(Emi_e, Hint)) ! A(me,ne,t+dt)
        BWH_e = -Ca*cross_prod(Emi_e, WH) - Cb*cross_prod(Emi_e, cross_prod(Emi_e, WH))     ! B(me,t+dt)*WH
        Emi   = Emi + 0.5*(A_e+A)*dt + 0.5*(BWH_e+BWH)                                      ! m + 0.5*[A(me,ne,t+dt)+A(m,n,t)]*dt + 0.5*[B(me,t+dt)+B(m,t)]*WH 
        Emi   = Emi / sqrt(dot_prod(Emi, Emi))                                              ! m/|m|
        
        Oint  = -MU0*Mui*HK * dot_prod(Emi_e, Eni_e) * cross_prod(Emi_e, Eni_e)             ! Oint(me,ne,t)
        C_e   = -(1.0/Zi) * cross_prod(Eni_e, Oint)                                         ! C(me,ne,t)
        DW0_e = -(1.0/Zi) * cross_prod(Eni_e, W0)                                           ! D(ne,t)*W0
        Eni   = Eni + 0.5*(C_e+C)*dt + 0.5*(DW0_e+DW0)                                      ! n + 0.5*[C(me,ne,t+dt)+C(m,n,t)]*dt + 0.5*[D(ne,t+dt)+D(n,t)]*W0
        Eni   = Eni / sqrt(dot_prod(Eni, Eni))                                              ! n/|n|

    return
    end subroutine stratonovich_heun

!--------------------------------------------------------------------------------------------------------------------------------------------------------------
  
    !! Evolution
    subroutine evolution(N, Mu, Em, En, Z, SH, S0, Ha, Hb, HK, alp, dt)

        ! Perform the evolution of the system in one time step.
        !
        ! Input:
        ! -              N (integer): Number of Particles       
        ! - Mu (real*8, array[N, 1]): Magnetic Moments (Magnitude) List        
        ! - Em (real*8, array[N, 3]): Magnetic Moments (Vector) List
        ! - En (real*8, array[N, 3]): Easy Axes List 
        ! -  Z (real*8, array[N, 1]): Drag Cointicients List        
        ! - SH (real*8, array[N, 1]): Thermal Field Standard Deviations List
        ! - S0 (real*8, array[N, 1]): Thermal Torque Standard Deviations List        
        ! - Ha (real*8, array[3, 1]): Magnetic Field -> H = H(t) 
        ! - Hb (real*8, array[3, 1]): Magnetic Field -> H = H(t+dt) 
        ! -              HK (real*8): Anisotropic Field Amplitude 
        ! -             alp (real*8): Damping Parameter      
        ! -              dt (real*8): Integration Time         
        !
        ! Output:  
        ! - None     
        !
        ! Used by:
        ! - llg-t.run_Microstates
        ! - llg-t.run_MvsH
        ! - llg-t.run_MvsT

        use constants, only    : G  
        integer, intent(in)   :: N
        real*8, intent(in)    :: Mu(0:N-1), Z(0:N-1), SH(0:N-1), S0(0:N-1), Ha(0:2), Hb(0:2), HK, alp, dt
        real*8, intent(inout) :: Em(0:N-1, 0:2), En(0:N-1, 0:2)
        real*8                :: Ca, Cb
        integer               :: i
        
#ifdef THREADS
    call omp_set_num_threads(THREADS)
#endif

        Ca = G / (1.0 + alp**2) ! Precession Constant 
        Cb = Ca * alp           ! Damping Constant
        
        !$omp parallel do private(i) shared(Mu, Em, En, Z, SH, S0, Ha, Hb, HK, Ca, Cb, dt)
        do i = 0, N-1
            call stratonovich_heun(Mu(i) ,Em(i, :), En(i, :), Z(i), SH(i), S0(i), Ha, Hb, HK, Ca, Cb, dt)
        end do
        !$omp end parallel do    
                    
    return
    end subroutine evolution
    
!--------------------------------------------------------------------------------------------------------------------------------------------------------------    
end module integration