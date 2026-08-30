module physics

    contains    
    
!-----------------------------------------------------------------------------------------------

        !! Temperature
        pure function T_(Ti, Tf, tt, t)

            ! Generate linearly time-dependent temperature.
            !
            ! Input:
            ! -  Ti (real*8): Initial Temperature         
            ! -  Tf (real*8): Final Temperature  
            ! -  tt (real*8): Total Time   
            ! -   t (real*8): Current Time
            !
            ! Output:  
            ! - T_ (real*8): Temperature     
            !
            ! Used by:
            ! - solvers.llg.run_MvsT
            ! - solvers.llg-t.run_MvsT
            !
            ! Last Updated: 
            ! - 16/08/2026

            real*8, intent(in) :: Ti, Tf, tt, t
            real*8             :: T_
            
            T_ = Ti + (Tf-Ti)/tt * t ! Linearly Time-Dependent Temperature
            
        end function T_         
    
!-----------------------------------------------------------------------------------------------

        !! Magnetic Field
        pure function H_(H0, f, t)

            ! Generate cosinusoidal time-dependent magnetic field in z-direction.
            !
            ! Input:
            ! -                 H0 (real*8): Magnetic Field Amplitude         
            ! -                  f (real*8): Magnetic Field Frecuency
            ! -                  t (real*8): Current Time         
            !
            ! Output:  
            ! - H_ ((real*8, ), array[3, ]): Magnetic Field        
            !
            ! Used by:
            ! - solvers.llg.run_Microstates
            ! - solvers.llg.run_MvsH
            ! - solvers.llg.run_MvsT
            ! - solvers.llg-t.run_Microstates
            ! - solvers.llg-t.run_MvsH
            ! - solvers.llg-t.run_MvsT
            !
            ! Last Updated: 
            ! - 16/08/2026

            use constants, only : PI          
            real*8, intent(in) :: H0, f, t
            real*8             :: H_(0:2)
            
            H_ = [0.0d0, 0.0d0, H0*cos(2.0*PI*f*t)] ! Cosenoidal Time-Dependent Magnetic Field
            
        end function H_           
                 
!-----------------------------------------------------------------------------------------------

        !! Solvent Viscosity
        function ETA_(T0)

            ! Generate the solvent vicosity based on the Vogel–Fulcher–Tammann model.
            !
            ! Input:
            ! -   T0 (real*8): Temperature              
            !
            ! Output:  
            ! - ETA_ (real*8): Solvent Viscosity   
            !
            ! Used by:
            ! - solvers.llg-t.run_Microstates
            ! - solvers.llg-t.run_MvsH
            ! - solvers.llg-t.run_MvsT
            !
            ! Last Updated: 
            ! - 16/08/2026
         
            real*8, intent(in) :: T0
            real*8             :: TM, T_MAX, ETA_
            
            TM    = 273.15 ! Melting Temperature 
            T_MAX = 373.0  ! Maximum Temperature
            
            if (T0 < TM) then  
                ETA_ = 1.0d99                                               ! Solvent Viscosity  
            else if (T0 >= TM .and. T0 <= T_MAX) then
                ETA_ = 1.0d-3 * exp(-3.7188)* exp(578.9190/(T0 - 137.5460)) ! Solvent Viscosity                 
            else
                print *, "Invalid Temperature!. Use T0 < 373.0 K."
                stop 
            end if
                      
        end function ETA_
        
!-----------------------------------------------------------------------------------------------

        !! Drag Coefficients
        subroutine Z_(N, Op, eta, Z)

            ! Generate a configuration of drag coefficients.
            !
            ! Input:
            ! -                 N (integer): Number of Particles
            ! - Op ((real*8, ), array[N, ]): Particle Volumes
            ! -                eta (real*8): Solvent Viscosity
            !
            ! Output:
            ! -  Z ((real*8, ), array[N, ]): Drag Coefficients
            !
            ! Used by:
            ! - solvers.llg-t.run_Microstates
            ! - solvers.llg-t.run_MvsH
            ! - solvers.llg-t.run_MvsT
            !
            ! Last Updated: 
            ! - 16/08/2026

            integer, intent(in) :: N
            real*8, intent(in)  :: Op(0:N-1), eta
            real*8, intent(out) :: Z(0:N-1)
            integer             :: i

            !$omp do private(i)
            do i = 0, N-1
                Z(i) = 6.0 * eta * Op(i) ! Drag Coefficient
            end do
            !$omp end do

        end subroutine Z_
    
!-----------------------------------------------------------------------------------------------

        !! Thermal Field Standard Deviations
        subroutine SH_(N, Mu, T0, alp, dt, SH)

            ! Generate a configuration of thermal field standard deviations.
            !
            ! Input:
            ! -                 N (integer): Number of Particles
            ! - Mu ((real*8, ), array[N, ]): Magnetic Moments (Magnitude)
            ! -                 T0 (real*8): Temperature
            ! -                alp (real*8): Damping Parameter
            ! -                 dt (real*8): Integration Time
            !
            ! Output:
            ! - SH ((real*8, ), array[N, ]): Thermal Field Standard Deviations
            !
            ! Used by:
            ! - solvers.llg.run_Microstates
            ! - solvers.llg.run_MvsH
            ! - solvers.llg.run_MvsT
            ! - solvers.llg-t.run_Microstates
            ! - solvers.llg-t.run_MvsH
            ! - solvers.llg-t.run_MvsT
            !
            ! Last Updated: 
            ! - 16/08/2026

            use constants, only  : KB, MU0, G
            integer, intent(in) :: N
            real*8, intent(in)  :: Mu(0:N-1), T0, alp, dt
            real*8, intent(out) :: SH(0:N-1)
            real*8              :: DH
            integer             :: i

            !$omp do private(i, DH)
            do i = 0, N-1
                DH    = ((KB*T0)/(MU0*Mu(i)*G)) * (alp/(1.0+alp**2)) ! Diffusion Coefficient
                SH(i) = sqrt(2.0*DH*dt)                              ! Standard Deviation
            end do
            !$omp end do

        end subroutine SH_
        
!-----------------------------------------------------------------------------------------------

        !! Thermal Torque Standard Deviations
        subroutine S0_(N, Z, T0, dt, S0)

            ! Generate a configuration of thermal torque standard deviations.
            !
            ! Input:
            ! -                   N (integer): Number of Particles
            ! -    Z ((real*8, ), array[N, ]): Drag Coefficients
            ! -                   T0 (real*8): Temperature
            ! -                   dt (real*8): Integration Time
            !
            ! Output:
            ! - S0 (((real*8, ), array[N, ])): Thermal Torque Standard Deviations
            !
            ! Used by:
            ! - solvers.llg-t.run_Microstates
            ! - solvers.llg-t.run_MvsH
            ! - solvers.llg-t.run_MvsT
            !
            ! Last Updated: 
            ! - 16/08/2026

            use constants, only  : KB
            integer, intent(in) :: N
            real*8, intent(in)  :: Z(0:N-1), T0, dt
            real*8, intent(out) :: S0(0:N-1)
            real*8              :: D0
            integer             :: i

            !$omp do private(i, D0)
            do i = 0, N-1
                D0    = KB*T0*Z(i)      ! Diffusion Coefficient
                S0(i) = sqrt(2.0*D0*dt) ! Standard Deviation
            end do
            !$omp end do

        end subroutine S0_
                              
!-----------------------------------------------------------------------------------------------

end module physics