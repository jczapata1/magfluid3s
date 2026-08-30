module integration

    contains
    
!------------------------------------------------------------------------------------------------------------------------------

    !! Stratonovich–Heun Algorithm
    subroutine stratonovich_heun(Emi, Eni, SHi, Ha, Hb, HK, Ca, Cb, dt)
    
        ! Perform the Stratonovich–Heun algorithm.
        !
        ! Input:        
        ! - Emi ((real*8, ), array[3, ]): ith-Magnetic Moment (Vector)
        ! - Eni ((real*8, ), array[3, ]): ith-Easy Axis
        ! -                 SHi (real*8): ith-Thermal Field Standard Deviation
        ! -  Ha ((real*8, ), array[3, ]): Magnetic Field -> H = H(t) 
        ! -  Hb ((real*8, ), array[3, ]): Magnetic Field -> H = H(t+dt)         
        ! -                  HK (real*8): Anisotropic Field Amplitude 
        ! -                  Ca (real*8): Damping Constant   
        ! -                  Cb (real*8): Damping Constant         
        ! -                  dt (real*8): Integration Time         
        !
        ! Output:
        ! - None
        !
        ! Used by:
        ! - solvers.llg.integration.evolution
        !
        ! Last Updated: 
        ! - 16/08/2026
        
        use math, only: rv_normal, dot_prod, cross_prod
        real*8, intent(in)    :: Eni(0:2), SHi, Ha(0:2), Hb(0:2), HK, Ca, Cb, dt
        real*8, intent(inout) :: Emi(0:2)
        real*8                :: Emi_e(0:2), WH(0:2), Hint(0:2), Hint_e(0:2), A(0:2), A_e(0:2), BWH(0:2), BWH_e(0:2)
        real*8                :: EmH(0:2), EmWH(0:2), EmH_e(0:2), EmWH_e(0:2)

        ! Thermal Noise
        WH = rv_normal(SHi)

        ! Euler Predictor
        Hint  = Ha + HK*dot_prod(Emi, Eni)*Eni             ! Hint(m,t)
        EmH   = cross_prod(Emi, Hint)                      ! m x Hint(m,t)
        A     = -Ca*EmH - Cb*cross_prod(Emi, EmH)          ! A(m,t)
        EmWH  = cross_prod(Emi, WH)                        ! m x WH
        BWH   = -Ca*EmWH - Cb*cross_prod(Emi, EmWH)        ! B(m,t)*WH
        Emi_e = Emi + A*dt + BWH                           ! m + A(m,t)*dt + B(m,t)*WH
        Emi_e = Emi_e / sqrt(dot_prod(Emi_e, Emi_e))       ! me/|me|

        ! Heun Predictor
        Hint_e = Hb + HK*dot_prod(Emi_e, Eni)*Eni          ! Hint(me,t+dt)
        EmH_e  = cross_prod(Emi_e, Hint_e)                 ! me x Hint(me,t+dt)
        A_e    = -Ca*EmH_e - Cb*cross_prod(Emi_e, EmH_e)   ! A(me,t+dt)
        EmWH_e = cross_prod(Emi_e, WH)                     ! me x WH
        BWH_e  = -Ca*EmWH_e - Cb*cross_prod(Emi_e, EmWH_e) ! B(me,t+dt)*WH
        Emi    = Emi + 0.5*(A_e+A)*dt + 0.5*(BWH_e+BWH)    ! m + 0.5*[A(me,t+dt)+A(m,t)]*dt + 0.5*[B(me,t+dt)+B(m,t)]*WH
        Emi    = Emi / sqrt(dot_prod(Emi, Emi))            ! m/|m|
        
    return
    end subroutine stratonovich_heun

!------------------------------------------------------------------------------------------------------------------------------

    !! Evolution
    subroutine evolution(N, Em, En, SH, Ha, Hb, HK, alp, dt)

        ! Perform the evolution of the system in one time step.
        !
        ! Input:
        ! -                        N (integer): Number of Particles
        ! - Em ((real*8, real*8), array[3, N]): Magnetic Moments (Vector)
        ! - En ((real*8, real*8), array[3, N]): Easy Axes
        ! -        SH ((real*8, ), array[3, ]): Thermal Field Standard Deviations
        ! -        Ha ((real*8, ), array[3, ]): Magnetic Field -> H = H(t)
        ! -        Hb ((real*8, ), array[3, ]): Magnetic Field -> H = H(t+dt)
        ! -                        HK (real*8): Anisotropic Field Amplitude
        ! -                       alp (real*8): Damping Parameter
        ! -                        dt (real*8): Integration Time
        !
        ! Output:
        ! - None
        !
        ! Used by:
        ! - solvers.llg.run_Microstates
        ! - solvers.llg.run_MvsH
        ! - solvers.llg.run_MvsT
        !
        ! Last Updated: 
        ! - 16/08/2026

        use constants, only    : G
        integer, intent(in)   :: N
        real*8, intent(in)    :: En(0:2, 0:N-1), SH(0:N-1), Ha(0:2), Hb(0:2), HK, alp, dt
        real*8, intent(inout) :: Em(0:2, 0:N-1)
        real*8                :: Ca, Cb
        integer               :: i

        ! Constants
        Ca = G / (1.0 + alp**2)
        Cb = Ca * alp

        !$omp do private(i)
        do i = 0, N-1
            call stratonovich_heun(Em(:, i), En(:, i), SH(i), Ha, Hb, HK, Ca, Cb, dt)
        end do
        !$omp end do    
                    
    return
    end subroutine evolution
    
!------------------------------------------------------------------------------------------------------------------------------   

end module integration