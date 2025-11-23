module integration

    contains
    
!---------------------------------------------------------------------------------------------------------------------------------------------------------

    !! Stratonovich–Heun Algorithm
    subroutine stratonovich_heun(Emi, Eni, SHi, Ha, Hb, HK, Ca, Cb, dt)
    
        ! Perform the Stratonovich–Heun algorithm.
        !
        ! Input:        
        ! - Emi (real*8, array[3, 1]): ith-Magnetic Moment (Vector)
        ! - Eni (real*8, array[3, 1]): ith-Easy Axis
        ! -              SHi (real*8): ith-Thermal Field Standard Deviation
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
        ! - integration.evolution
        
        use math, only: rv_normal, dot_prod, cross_prod
        real*8, intent(in)    :: Eni(0:2), SHi, Ha(0:2), Hb(0:2), HK, Ca, Cb, dt
        real*8, intent(inout) :: Emi(0:2)
        real*8                :: Emi_e(0:2), WH(0:2), Hint(0:2), A(0:2), A_e(0:2), BWH(0:2), BWH_e(0:2)

        ! Thermal Noise
        WH = rv_normal(SHi)
    
        ! Euler Predictor   
        Hint  = Ha + HK*dot_prod(Emi, Eni)*Eni                                              ! Hint(m,t) 
        A     = -Ca*cross_prod(Emi, Hint) - Cb*cross_prod(Emi, cross_prod(Emi, Hint))       ! A(m,t) 
        BWH   = -Ca*cross_prod(Emi, WH) - Cb*cross_prod(Emi, cross_prod(Emi, WH))           ! B(m,t)*WH
        Emi_e = Emi + A*dt + BWH                                                            ! m + A(m,t)*dt + B(m,t)*WH 
        Emi_e = Emi_e / sqrt(dot_prod(Emi_e, Emi_e))                                        ! me/|me|
        
        ! Heun Predictor 
        Hint  = Hb + HK*dot_prod(Emi_e, Eni)*Eni                                            ! Hint(me,t+dt)
        A_e   = -Ca*cross_prod(Emi_e, Hint) - Cb*cross_prod(Emi_e, cross_prod(Emi_e, Hint)) ! A(me,t+dt)
        BWH_e = -Ca*cross_prod(Emi_e, WH) - Cb*cross_prod(Emi_e, cross_prod(Emi_e, WH))     ! B(me,t+dt)*WH
        Emi   = Emi + 0.5*(A_e+A)*dt + 0.5*(BWH_e+BWH)                                      ! m + 0.5*[A(me,t+dt)+A(m,t)]*dt + 0.5*[B(me,t+dt)+B(m,t)]*WH 
        Emi   = Emi / sqrt(dot_prod(Emi, Emi))                                              ! m/|m|
        
    return
    end subroutine stratonovich_heun

!---------------------------------------------------------------------------------------------------------------------------------------------------------

    !! Evolution
    subroutine evolution(N, Em, En, SH, Ha, Hb, HK, alp, dt)

        ! Perform the evolution of the system in one time step.
        !
        ! Input:
        ! -              N (integer): Number of Particles          
        ! - Em (real*8, array[N, 3]): Magnetic Moments (Vector) List
        ! - En (real*8, array[N, 3]): Easy Axes List  
        ! -    SH (real*8, array[N]): Thermal Field Standard Deviations List
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
        ! - llg.run_Microstates
        ! - llg.run_MvsH
        ! - llg.run_MvsT

        use constants, only    : G  
        integer, intent(in)   :: N
        real*8, intent(in)    :: En(0:N-1, 0:2), SH(0:N-1), Ha(0:2), Hb(0:2), HK, alp, dt
        real*8, intent(inout) :: Em(0:N-1, 0:2)
        real*8                :: Ca, Cb
        integer               :: i
        
#ifdef THREADS
    call omp_set_num_threads(THREADS)
#endif

        Ca = G / (1.0 + alp**2) ! Precession Constant 
        Cb = Ca * alp           ! Damping Constant

        !$omp parallel do private(i) shared(Em, En, SH, Ha, Hb, HK, Ca, Cb, dt)
        do i = 0, N-1
            call stratonovich_heun(Em(i, :), En(i, :), SH(i), Ha, Hb, HK, Ca, Cb, dt)
        end do
        !$omp end parallel do    
                    
    return
    end subroutine evolution
    
!---------------------------------------------------------------------------------------------------------------------------------------------------------   

end module integration