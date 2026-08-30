module integration

    contains
    
!---------------------------------------------------------------------------------------------------------------------------------------------------

    !! Stratonovich–Heun Algorithm
    subroutine stratonovich_heun(Mui, Emi, Eni, Zi, SHi, S0i, Ha, Hb, HK, Ca, Cb, dt)

        ! Perform the Stratonovich–Heun algorithm.
        !
        ! Input:   
        ! -                 Mui (real*8): ith-Magnetic Moment (Magnitude)        
        ! - Emi ((real*8, ), array[3, ]): ith-Magnetic Moment (Vector)
        ! - Eni ((real*8, ), array[3, ]): ith-Easy Axis
        ! -                  Zi (real*8): ith-Drag Cointicient          
        ! -                 SHi (real*8): ith-Thermal Field Standard Deviation
        ! -                 S0i (real*8): ith-Thermal Torque Standard Deviation        
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
        ! - solvers.llg-t.integration.evolution
        !
        ! Last Updated: 
        ! - 16/08/2026

        use constants, only: MU0
        use math, only: rv_normal, dot_prod, cross_prod 
        real*8, intent(in)    :: Mui, Zi, SHi, S0i, Ha(0:2), Hb(0:2), HK, Ca, Cb, dt
        real*8, intent(inout) :: Emi(0:2), Eni(0:2)
        real*8                :: Emi_e(0:2), WH(0:2), Hint(0:2), Hint_e(0:2), A(0:2), A_e(0:2), BWH(0:2), BWH_e(0:2)
        real*8                :: Eni_e(0:2), W0(0:2), Oint(0:2), Oint_e(0:2), C(0:2), C_e(0:2), DW0(0:2), DW0_e(0:2)
        real*8                :: EmH(0:2), EmWH(0:2), EmH_e(0:2), EmWH_e(0:2)

        ! Thermal Noise
        WH = rv_normal(SHi)
        W0 = rv_normal(S0i)

        ! Em-Euler Predictor
        Hint  = Ha + HK*dot_prod(Emi, Eni)*Eni                                   ! Hint(m,n,t)
        EmH   = cross_prod(Emi, Hint)                                            ! m x Hint(m,n,t)
        A     = -Ca*EmH - Cb*cross_prod(Emi, EmH)                                ! A(m,n,t)
        EmWH  = cross_prod(Emi, WH)                                              ! m x WH
        BWH   = -Ca*EmWH - Cb*cross_prod(Emi, EmWH)                              ! B(m,t)*WH
        Emi_e = Emi + A*dt + BWH                                                 ! m + A(m,n,t)*dt + B(m,t)*WH
        Emi_e = Emi_e / sqrt(dot_prod(Emi_e, Emi_e))                             ! me/|me|

        ! En-Euler Predictor
        Oint  = -MU0*Mui*HK * dot_prod(Emi, Eni) * cross_prod(Emi, Eni)          ! Oint(m,n,t)
        C     = -(1.0/Zi) * cross_prod(Eni, Oint)                                ! C(m,n,t)
        DW0   = -(1.0/Zi) * cross_prod(Eni, W0)                                  ! D(n,t)*W0
        Eni_e = Eni + C*dt + DW0                                                 ! n + C(m,n,t)*dt + D(n,t)*W0
        Eni_e = Eni_e / sqrt(dot_prod(Eni_e, Eni_e))                             ! ne/|ne|

        ! Em-Heun Predictor
        Hint_e = Hb + HK*dot_prod(Emi_e, Eni_e)*Eni_e                            ! Hint(me,ne,t+dt)
        EmH_e  = cross_prod(Emi_e, Hint_e)                                       ! me x Hint(me,ne,t+dt)
        A_e    = -Ca*EmH_e - Cb*cross_prod(Emi_e, EmH_e)                         ! A(me,ne,t+dt)
        EmWH_e = cross_prod(Emi_e, WH)                                           ! me x WH
        BWH_e  = -Ca*EmWH_e - Cb*cross_prod(Emi_e, EmWH_e)                       ! B(me,t+dt)*WH
        Emi    = Emi + 0.5*(A_e+A)*dt + 0.5*(BWH_e+BWH)                          ! m + 0.5*[A(me,ne,t+dt)+A(m,n,t)]*dt + 0.5*[B(me,t+dt)+B(m,t)]*WH
        Emi    = Emi / sqrt(dot_prod(Emi, Emi))                                  ! m/|m|

        ! En-Heun Predictor
        Oint_e = -MU0*Mui*HK * dot_prod(Emi_e, Eni_e) * cross_prod(Emi_e, Eni_e) ! Oint(me,ne,t)
        C_e    = -(1.0/Zi) * cross_prod(Eni_e, Oint_e)                           ! C(me,ne,t)
        DW0_e  = -(1.0/Zi) * cross_prod(Eni_e, W0)                               ! D(ne,t)*W0
        Eni    = Eni + 0.5*(C_e+C)*dt + 0.5*(DW0_e+DW0)                          ! n + 0.5*[C(me,ne,t+dt)+C(m,n,t)]*dt + 0.5*[D(ne,t+dt)+D(n,t)]*W0
        Eni    = Eni / sqrt(dot_prod(Eni, Eni))                                  ! n/|n|

    return
    end subroutine stratonovich_heun

!---------------------------------------------------------------------------------------------------------------------------------------------------
  
    !! Evolution
    subroutine evolution(N, Mu, Em, En, Z, SH, S0, Ha, Hb, HK, alp, dt)

        ! Perform the evolution of the system in one time step.
        !
        ! Input:
        ! -                        N (integer): Number of Particles
        ! -        Mu ((real*8, ), array[3, ]): Magnetic Moments (Magnitude)
        ! - Em ((real*8, real*8), array[3, N]): Magnetic Moments (Vector)
        ! - En ((real*8, real*8), array[3, N]): Easy Axes
        ! -         Z ((real*8, ), array[3, ]): Drag Coefficients
        ! -        SH ((real*8, ), array[3, ]): Thermal Field Standard Deviations
        ! -        S0 ((real*8, ), array[3, ]): Thermal Torque Standard Deviations
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
        ! - solvers.llg-t.run_Microstates
        ! - solvers.llg-t.run_MvsH
        ! - solvers.llg-t.run_MvsT
        !
        ! Last Updated: 
        ! - 16/08/2026

        use constants, only    : G
        integer, intent(in)   :: N
        real*8, intent(in)    :: Mu(0:N-1), Z(0:N-1), SH(0:N-1), S0(0:N-1), Ha(0:2), Hb(0:2), HK, alp, dt
        real*8, intent(inout) :: Em(0:2, 0:N-1), En(0:2, 0:N-1)
        real*8                :: Ca, Cb
        integer               :: i

        ! Constants
        Ca = G / (1.0 + alp**2)
        Cb = Ca * alp

        !$omp do private(i)
        do i = 0, N-1
            call stratonovich_heun(Mu(i), Em(:, i), En(:, i), Z(i), SH(i), S0(i), Ha, Hb, HK, Ca, Cb, dt)
        end do
        !$omp end do    
                    
    return
    end subroutine evolution
    
!---------------------------------------------------------------------------------------------------------------------------------------------------

end module integration